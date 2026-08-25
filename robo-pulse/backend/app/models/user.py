'''
Robopulse Command Center Day 5 - User entity 
This is not a part of the original ERD as shown in the problem statement document, but it is required
to fulfill the RBAC section of the document. Every request from here forward must know who is asking 
and what role they have
'''

from __future__ import annotations
from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    #storing password hash instead of raw
    hashed_password: Mapped[str] = mapped_column(String(255))

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls]
        )
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return (f"User(id={self.id}, username={self.username!r}, role={self.role.value})")