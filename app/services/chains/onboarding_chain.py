from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sqlalchemy.orm import Session
from app.models.userdata import Userdata
from app.core.config import OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0.2, api_key=OPENAI_API_KEY)

# 사용자 온보딩 체인 (레벨 + 선호 정보 설정)
onboarding_prompt = PromptTemplate(
    input_variables=["intro_message"],
    template=(
        "You are an onboarding assistant for an English learning app.\n"
        "Ask the user their English level (choose from: Beginner, Intermediate, Advanced)\n"
        "and what word information they want to see (choose from: definition, example, ipa, related_words, part_of_speech, synonyms, antonyms, frequency, etymology, translation, collocations, mnemonic, usage_note, register, image).\n"
        "Always include \"word\" and \"korean_meaning\" in the preferred_fields regardless of the user's input.\n"
        "After the user answers, extract only the structured data.\n"
        "Respond ONLY in this JSON format (no explanations):\n"
        "{{\"user_level\": \"...\", \"preferred_fields\": [\"...\"]}}\n"
        "User: {intro_message}"
    )
)

# Runnable chain으로 연결
onboarding_chain = onboarding_prompt | llm

# DB에 사용자 설정 저장
def save_user_onboarding(db: Session, user_id: int, info: dict):
    userdata = db.query(Userdata).filter(Userdata.user_id == user_id).first()
    if userdata:
        userdata.user_level = info.get("user_level")
        userdata.preferred_fields = info.get("preferred_fields", [])
        db.commit()


"""
# Optional: 단독 테스트
if __name__ == "__main__":
    intro = "Hi! I'm an intermediate learner and I want definitions and examples only."
    result = onboarding_chain.invoke({"intro_message": intro})
    print("\n[Onboarding Result]\n", result)
"""
