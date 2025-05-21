from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from langdetect import detect
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.chathistory import ChatHistory
from app.models.userdata import Userdata

client = OpenAI(api_key=OPENAI_API_KEY)

# 언어 감지 함수
def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def get_last_n_messages(db: Session, user_id: int, n: int = 6):
    records = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(n)
        .all()
    )
    return [
        {"role": r.role, "content": r.content}
        for r in reversed(records)
    ]


def save_message(db: Session, user_id: int, role: str, content: str):
    msg = ChatHistory(user_id=user_id, role=role, content=content, timestamp=datetime.utcnow())
    db.add(msg)
    db.commit()


def update_learned_words(db: Session, user_id: int, new_entries: list[dict]):
    userdata = db.query(Userdata).filter(Userdata.user_id == user_id).first()
    if userdata:
        current = userdata.learned_words or []
        word_map = {entry['word']: entry for entry in current}
        for entry in new_entries:
            word_map[entry['word']] = entry
        userdata.learned_words = list(word_map.values())
        db.commit()


def ask_gpt(user_input: str, user_id: int, db: Session) -> str:
    messages = get_last_n_messages(db, user_id)

    system_prompt = {
        "role": "system",
        "content": (
            "You are a friendly and professional English tutor AI who helps the user learn and retain English vocabulary and expressions naturally. "
        "Always consider the user's English proficiency level and previously learned vocabulary when providing answers. "
        "If the user's question is about a vocabulary word, respond in JSON format with the following fields: word, definition, example, ipa, and optionally related_words. "
        "Only include fields the user has requested before, if known. "
        "respond in the same language the user used"
        "If the user is engaging in casual conversation, reply in natural, friendly respond without using JSON."
        "If the question is unclear or ambiguous, politely ask for clarification instead of guessing."
        )
    }
    messages.insert(0, system_prompt)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    answer = response.choices[0].message.content

    save_message(db, user_id, "user", user_input)
    save_message(db, user_id, "assistant", answer)

    try:
        parsed = eval(answer)  # 실제 서비스에선 json.loads()나 pydantic 쓰는 게 안전
        if isinstance(parsed, list):
            update_learned_words(db, user_id, parsed)
        elif isinstance(parsed, dict):
            update_learned_words(db, user_id, [parsed])
    except Exception as e:
        print("[WARN] GPT 응답 파싱 실패:", e)

    return answer

"""
def ask_gpt(user_message: str, learned_words: list[str], prompt_template: str) -> str:
    memory = ", ".join(learned_words) if learned_words else "None"
    language = detect_language(user_message)

    # 필요 시 prompt_template 안에 언어 관련 변수 넣는 것도 가능
    prompt = prompt_template.format(language=language)

    messages = [
        {
            "role": "system",
            "content": "너는 친절하고 유능한 영어 튜터야"
        },
        {
            "role": "user",
            "content": (
                f"User level: Intermediate\n"
                f"Previously learned expressions: {memory}\n"
                f"User message: {user_message}\n"
                f"Please answer appropriately. "
                f"If it's a vocabulary question, return a summary in JSON format "
                f"with: keyword, definition, example, IPA (optional), related_words (optional)."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 'gpt-4'로 변경 가능
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
    #return str(response.choices[0].message.content)
"""
