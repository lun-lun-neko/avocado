from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import Users
from app.models.userdata import Userdata

# 1. 테이블 자동 생성 시도 (이미 있으면 무시)
Base.metadata.create_all(bind=engine)

# 2. 세션 열고 쿼리 테스트
db = SessionLocal()

try:
    users = db.query(Users).all()
    print("✅ 연결 성공! 유저 수:", len(users))
except Exception as e:
    print("❌ 연결 실패:", e)
finally:
    db.close()