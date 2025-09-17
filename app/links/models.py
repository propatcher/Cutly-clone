from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey,Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.clicks.models import Click

class Link(Base):
    __tablename__ = 'links'
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    short_code : Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    original_url : Mapped[str] = mapped_column(String(255), nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    clicks_count : Mapped[int] = mapped_column(Integer, default=0)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship("User", back_populates="links")
    clicks: Mapped[list["Click"]] = relationship("Click", back_populates="links")    