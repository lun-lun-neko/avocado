from typing import Optional, List
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.userdata import Userdata
from app.models.chathistory import  ChatHistory

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(100))

    userdata: Mapped[List['Userdata']] = relationship(
        'Userdata', back_populates='user', cascade="all, delete"
    )
    chathistory: Mapped[List['ChatHistory']] = relationship('ChatHistory', back_populates='user')