from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from app.infrastructure.models.incident import IncidentCategory

class CreateIncidentRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    category: IncidentCategory

class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: str
    category: IncidentCategory
    created_at: datetime
    owner_id: UUID

    class Config:
        from_attributes = True
