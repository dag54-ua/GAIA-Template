from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SAEnum, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

class IncidentCategory(str, Enum):
    CLEANING = "CLEANING"
    NOISE = "NOISE"
    MAINTENANCE = "MAINTENANCE"
    SECURITY = "SECURITY"

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[IncidentCategory] = mapped_column(SAEnum(IncidentCategory), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships can be added later if needed, e.g.:
    # owner = relationship("User", back_populates="incidents")
