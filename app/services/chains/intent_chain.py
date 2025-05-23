from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.core.config import OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4", temperature=0.0, api_key=OPENAI_API_KEY)

intent_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You're an intent classifier for an English learning assistant.\n"
        "Classify the user's message into one of the following categories:\n"
        "- 'vocab': asking about a word's meaning, example, or pronunciation\n"
        "- 'grammar': asking about grammar rules or sentence structure\n"
        "- 'translation': asking to translate between Korean and English\n"
        "- 'correction': asking if a sentence is grammatically correct\n"
        "- 'quiz': requesting a vocabulary or grammar quiz\n"
        "- 'conversation': general chat or casual conversation\n"
        "- 'other': anything unrelated to English learning\n\n"
        "User message: {message}\n"
        "Answer with only one word: vocab, grammar, translation, correction, quiz, conversation, or other."
    )
)

# 최신 방식으로 체인 생성
intent_chain = intent_prompt | llm

"""
# Optional: 테스트 실행
if __name__ == "__main__":
    test_inputs = [
        "What does resilient mean?",
        "Can you explain the present perfect?",
        "Translate 'apple' into Korean.",
        "Is this sentence correct: He go to school?",
        "Quiz me on phrasal verbs.",
        "How's your day going?",
        "What is LangChain?"
    ]

    for msg in test_inputs:
        result = intent_chain.invoke({"message": msg})
        print(f"\n[User] {msg}\n[Intent] {result.content.strip()}")
"""