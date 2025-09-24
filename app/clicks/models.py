from sqlalchemy import DateTime, ForeignKey,Integer, String
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

def utc_now():
    return datetime.now(timezone.utc)

class Click(Base):
    __tablename__ = 'clicks'
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    link_id : Mapped[int] = mapped_column(ForeignKey('links.id'))
    ip_address: Mapped[str] = mapped_column(String(255),nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255))
    clicked_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    links: Mapped["Link"] = relationship("Link", back_populates="clicks")