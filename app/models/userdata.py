from typing import Optional
from sqlalchemy import Integer, JSON, ForeignKey, ForeignKeyConstraint, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import Users  # 타입 힌트용

class Userdata(Base):
    __tablename__ = 'userdata'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    learned_words: Mapped[Optional[dict]] = mapped_column(JSON)
    user_level: Mapped[Optional[str]] = mapped_column(String(20))

    user: Mapped['Users'] = relationship('Users', back_populates='userdata')