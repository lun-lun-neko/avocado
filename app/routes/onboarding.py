from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json
from app.core.database import get_db
from app.services.chains.onboarding_chain import onboarding_chain, save_user_onboarding

router = APIRouter()

class OnboardingRequest(BaseModel):
    user_id: int
    intro_message: str

class OnboardingResponse(BaseModel):
    user_level: str
    preferred_fields: list[str]


@router.post("/onboarding", response_model=OnboardingResponse)
def run_onboarding(data: OnboardingRequest, db: Session = Depends(get_db)):
    # GPT 응답 생성
    result = onboarding_chain.invoke({"intro_message": data.intro_message})
    print("[GPT RAW RESPONSE]", result)

    try:
        parsed = json.loads(result.content)
        save_user_onboarding(db, data.user_id, parsed)
        return parsed
    except Exception as e:
        print("[Onboarding Parsing Error]", e)
        raise ValueError("Failed to parse onboarding response. Please try again.")
