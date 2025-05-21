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
