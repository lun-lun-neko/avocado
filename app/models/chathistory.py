from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, ForeignKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import Users  # 타입 힌트용
class ChatHistory(Base):
    __tablename__ = "chat_history"
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(10))  # 'user' or 'assistant'
    content: Mapped[str] = mapped_column(String(2000))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped['Users'] = relationship('Users', back_populates='chathistory')