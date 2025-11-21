from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Column, DateTime
from app.db.database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class Attractions(Base):
    __tablename__ = 'attractions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    cover_image: Mapped[str] = mapped_column(String(200), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)