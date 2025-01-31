from typing import Optional, Self

from app import db
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID


class Account(db.Model, UserMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(
        UUID(as_uuid=True), unique=True, nullable=False, server_default=text("uuid_generate_v4()")
    )
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime, server_default=db.text("CURRENT_TIMESTAMP"), onupdate=db.func.now()
    )

    def __init__(self, email, password, is_admin=False) -> None:
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.email}"

    @classmethod
    def find_by_email(cls, email: str) -> Optional[Self]:
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> list[Self]:
        return cls.query.all()
