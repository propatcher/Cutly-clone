from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import Boolean, DateTime, ForeignKey,Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(255),nullable=False,unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    links: Mapped[list["Link"]] = relationship("Link", back_populates='user')   