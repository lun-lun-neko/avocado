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
        "Examples:\n"
        "- '단어의 뜻 알려줘' → 'vocab'\n"
        "- 'post 단어 알려줘' → 'vocab'\n"
        "- 'resilient 무슨 뜻이야?' → 'vocab'\n"
        "- 'ubiquitous 뜻과 예문 알려줘' → 'vocab'\n"
        "- 'elated 발음이랑 뜻 설명해줘' → 'vocab'\n"
        "- 'elated 설명해줘' → 'vocab'\n"
        "- '‘empathy’ 예문 좀 줘' → 'vocab'\n"
        "- '‘impact’ 유의어/반의어 알려줘' → 'vocab'\n"
        "- 'recommend 뜻이 뭐야?' → 'vocab'\n"
        "- '문법 설명해줘' → 'grammar'\n"
        "- '현재완료랑 과거형 차이 뭐야?' → 'grammar'\n"
        "- '영어에서 가정법이 뭔데?' → 'grammar'\n"
        "- '수동태 어떻게 만들어?' → 'grammar'\n"
        "- '문장구조 SVOC 설명해줘' → 'grammar'\n"
        "- 'when과 while 차이점이 뭐야?' → 'grammar'\n"
        "- '영어로 번역해줘' → 'translation'\n"
        "- '‘나는 오늘 바빠’를 영어로 번역해줘' → 'translation'\n"
        "- '‘take it easy’는 무슨 뜻이야?' → 'translation'\n"
        "- 'You only live once를 한국어로 번역해줘' → 'translation'\n"
        "- '이 문장 한글로 바꿔줘: “Knowledge is power.”' → 'translation'\n"
        "- '이 문장 맞는 말이야? “He go to school.”' → 'correction'\n"
        "- '문법적으로 틀린 문장이야? “I has a car.”' → 'correction'\n"
        "- '아래 문장 자연스럽게 고쳐줘' → 'correction'\n"
        "- '내 문장 좀 교정해줘: “I very like this movie.”' → 'correction'\n"
        "- '단어 퀴즈 내줘' → 'quiz'\n"
        "- '문법 퀴즈 만들어줘' → 'quiz'\n"
        "- '토익에 자주 나오는 단어로 문제 줘' → 'quiz'\n"
        "- '예문 완성하는 퀴즈 줘' → 'quiz'\n"
        "- 'irregular verbs 퀴즈 부탁해' → 'quiz'\n"
        "- '오늘 어땠어?' → 'conversation'\n"
        "- 'GPT야 밥 먹었니?' → 'conversation'\n"
        "- '영어 공부 힘들어ㅠㅠ' → 'conversation'\n"
        "- '요즘 뭐 재밌는 일 있어?' → 'conversation'\n"
        "- '날씨가 좋아서 기분이 좋네~' → 'conversation'\n"
        "- 'LangChain이 뭐야?' → 'other'\n"
        "- '너는 어디서 작동하니?' → 'other'\n"
        "- '지금 시간 알려줘' → 'other'\n"
        "- '계산기 좀 해줘: 3765 × 2941' → 'other'\n"
        "- '채팅 기록 삭제해줘' → 'other'\n"
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