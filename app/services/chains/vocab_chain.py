from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session
from app.models.userdata import Userdata
from app.core.config import OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0.2, api_key=OPENAI_API_KEY)

# 사용자 선호 필드를 기반으로 프롬프트 생성
def build_vocab_chain(preferred_fields: list[str]):
    fields_string = ", ".join(preferred_fields)
    field_lines = "\n".join([f"  \"{field}\": ..." for field in preferred_fields])

    prompt = PromptTemplate(
        input_variables=["message"],
        template=(
            "You are an English vocabulary tutor.\n"
            "The user will send a message asking about a word (the message may contain Korean and may not be just the word).\n"
            "Your job is to identify the intended English word, and explain it clearly.\n"
            f"Respond in JSON format, including only the following fields: {fields_string}.\n"
            "Respond only in this structure:\n"
            "{{\n"
            f"{field_lines}\n"
            "}}\n"
            "User message: {message}"
        )
    )
    return prompt | llm


# DB에서 사용자 선호 필드 가져오기
def get_user_preferred_fields(db: Session, user_id: int) -> list[str]:
    userdata = db.query(Userdata).filter(Userdata.user_id == user_id).first()
    return userdata.preferred_fields if userdata and userdata.preferred_fields else ["word", "definition", "example"]

"""
# Optional: 단독 실행 테스트
if __name__ == "__main__":
    preferred_fields = ["word", "definition", "ipa"]
    chain = build_vocab_chain(preferred_fields)

    test_words = ["resilient", "ubiquitous"]
    for word in test_words:
        result = chain.invoke({"word": word})
        print(f"\n[Word] {word}\n[Response]\n{result.content.strip()}")
"""