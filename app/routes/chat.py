from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db, engine
from app.services.chains.intent_chain import intent_chain
from app.services.chains.vocab_chain import build_vocab_chain, get_user_preferred_fields

from langchain_openai import ChatOpenAI
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from app.core.config import OPENAI_API_KEY

router = APIRouter()

# ✅ 요청 데이터 모델 정의
class ChatRequest(BaseModel):
    user_id: int
    message: str

# ✅ 응답 데이터 모델 정의
class ChatResponse(BaseModel):
    intent: str
    response: str

# ✅ LLM 설정
general_llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=OPENAI_API_KEY)

# ✅ 사용자별 메모리 체인 구성
def get_conversation_chain(user_id: int):
    session_id = f"user-{user_id}"
    message_history = SQLChatMessageHistory(session_id=session_id, connection=engine)
    memory = ConversationBufferMemory(chat_memory=message_history, return_messages=True)
    return ConversationChain(llm=general_llm, memory=memory, verbose=False), memory

@router.post("/chat", response_model=ChatResponse)
def chat_with_gpt(request: ChatRequest, db: Session = Depends(get_db)):
    user_message = request.message
    user_id = request.user_id

    # 1. 의도 분류
    intent_result = intent_chain.invoke({"message": user_message})
    intent = intent_result.content.strip()

    # 2. 공통 메모리 체인 생성
    conversation_chain, memory = get_conversation_chain(user_id)

    # 3. 단어 설명 요청일 경우
    if intent == "vocab":
        preferred_fields = get_user_preferred_fields(db, user_id)
        vocab_chain = build_vocab_chain(preferred_fields)
        vocab_chain_with_memory = vocab_chain | memory
        vocab_result = vocab_chain_with_memory.invoke({"word": user_message})
        return ChatResponse(intent=intent, response=vocab_result.content.strip())

    # 4. 문법, 번역, 문장 교정 요청일 경우
    if intent in ["grammar", "translation", "correction"]:
        gpt_response = conversation_chain.invoke(user_message)
        if isinstance(gpt_response, dict) and "content" in gpt_response:
            return ChatResponse(intent=intent, response=gpt_response["content"].strip())
        return ChatResponse(intent=intent, response=str(gpt_response).strip())

    # 5. 퀴즈 요청일 경우
    if intent == "quiz":
        quiz_prompt = f"Create a short 3-question English quiz based on this request: '{user_message}'"
        quiz_response = conversation_chain.invoke(quiz_prompt)
        if isinstance(quiz_response, dict) and "content" in quiz_response:
            return ChatResponse(intent=intent, response=quiz_response["content"].strip())
        return ChatResponse(intent=intent, response=str(quiz_response).strip())

    # 6. 일상 대화일 경우
    if intent == "conversation":
        casual_prompt = f"Respond casually and naturally to: '{user_message}'"
        casual_response = conversation_chain.invoke(casual_prompt)
        if isinstance(casual_response, dict) and "content" in casual_response:
            return ChatResponse(intent=intent, response=casual_response["content"].strip())
        return ChatResponse(intent=intent, response=str(casual_response).strip())

    # 7. 기타 처리
    return ChatResponse(intent=intent, response="죄송합니다. 해당 요청은 이해하지 못했습니다.")











"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.services.chains.intent_chain import intent_chain
from app.services.chains.vocab_chain import build_vocab_chain, get_user_preferred_fields

from langchain_openai import ChatOpenAI
from app.core.config import OPENAI_API_KEY

router = APIRouter()

# 요청 데이터 모델 정의
class ChatRequest(BaseModel):
    user_id: int
    message: str

# 응답 데이터 모델 정의
class ChatResponse(BaseModel):
    intent: str
    response: str

# 일반 대화용 LLM
general_llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=OPENAI_API_KEY)

@router.post("/chat", response_model=ChatResponse)
def chat_with_gpt(request: ChatRequest, db: Session = Depends(get_db)):
    user_message = request.message
    user_id = request.user_id

    # 1. 의도 분류
    intent_result = intent_chain.invoke({"message": user_message})
    intent = intent_result.content.strip()

    # 2. 단어 설명 요청일 경우
    if intent == "vocab":
        preferred_fields = get_user_preferred_fields(db, user_id)
        vocab_chain = build_vocab_chain(preferred_fields)
        vocab_result = vocab_chain.invoke({"word": user_message})
        return ChatResponse(intent=intent, response=vocab_result.content.strip())

    # 3. 문법, 번역, 문장 교정 요청일 경우
    if intent in ["grammar", "translation", "correction"]:
        gpt_response = general_llm.invoke(user_message)
        return ChatResponse(intent=intent, response=gpt_response.content.strip())

    # 4. 퀴즈 요청일 경우
    if intent == "quiz":
        quiz_prompt = f"Create a short 3-question English quiz based on this request: '{user_message}'"
        quiz_response = general_llm.invoke(quiz_prompt)
        return ChatResponse(intent=intent, response=quiz_response.content.strip())

    # 5. 일상 대화일 경우
    if intent == "conversation":
        casual_prompt = f"Respond casually and naturally to: '{user_message}'"
        casual_response = general_llm.invoke(casual_prompt)
        return ChatResponse(intent=intent, response=casual_response.content.strip())

    # 6. 그 외 기타
    return ChatResponse(intent=intent, response="죄송합니다. 해당 요청은 이해하지 못했습니다.")

"""






"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import Users
from app.models.userdata import Userdata
from app.services.openai_service import ask_gpt
from app.core.database import get_db
from typing import Optional
import json

router = APIRouter()

class ChatRequest(BaseModel):
    user_message: str

@router.post("/chat")
def chat_with_gpt(request: ChatRequest, db: Session = Depends(get_db)):
    return {"gpt_response": ask_gpt(request.user_message, user_id=1, db=db)}
    
"""# chain 없는 버전


""""
#userdata 모델
class UserdataResponse(BaseModel):
    id: int
    messagelist: list
    wordlist: list

    model_config = {
        "from_attributes": True
    }


# 요청 모델
class ChatRequest(BaseModel):
    user_id: int
    user_message: str

# 응답 모델
class ChatResponse(BaseModel):
    gpt_response: str

# 요약 JSON 뽑는 함수
def extract_summary_from_response(gpt_content: str) -> dict:
    try:
        start = gpt_content.find('```json')
        end = gpt_content.find('```', start + 1)
        if start == -1 or end == -1:
            return {}    #영단어 관련 답변이 아니면 저장x
        json_str = gpt_content[start+7:end].strip()
        summary = json.loads(json_str)
        return summary
    except Exception as e:
        print("요약 파싱 실패:", str(e))
        return {}

# 진짜 /chat POST API
@router.post("/chat", response_model=ChatResponse)
def chat_with_gpt(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. 유저 확인
    user = db.query(Users).filter(Users.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. userdata 가져오기
    userdata = db.query(Userdata).filter(Userdata.user_id == user.id).first()
    if not userdata:
        raise HTTPException(status_code=404, detail="Userdata not found")

    # 3. messagelist 가져오기 (없으면 새로 생성)
    messages = userdata.messagelist or []

    # 4. wordlist에서 learned_words 추출
    learned_words = []
    if userdata.wordlist:
        learned_words = [word.get("keyword") for word in userdata.wordlist if "keyword" in word]

    # 5. messagelist에 새 질문 추가
    messages.append({
        "role": "user",
        "content": request.user_message
    })

    # 6. GPT 호출 (user_message, learned_words 사용)
    gpt_response = ask_gpt(
        user_message=request.user_message,
        learned_words=learned_words,
        prompt_template=user.prompt_template or "You are a friendly English tutor. Please explain clearly."
    ) #뒤엔 defalut 프롬프트?

    # 7. messagelist에 GPT 응답 추가
    messages.append({
        "role": "assistant",
        "content": gpt_response
    })

    # 8. messagelist 업데이트
    userdata.messagelist = messages

    # 9. 요약 JSON 뽑아서 wordlist 업데이트
    summary = extract_summary_from_response(gpt_response)
    if summary and "keyword" in summary and "definition" in summary:
        wordlist = userdata.wordlist or []
        wordlist.append(summary)
        userdata.wordlist = wordlist

    # 10. DB 커밋
    db.add(userdata)
    db.commit()

    # 11. 최종 응답 보내기
    return ChatResponse(gpt_response=gpt_response)
    

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    userdata: list[UserdataResponse]

# 일반 유저 조회: /user/{user_id}
@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""
