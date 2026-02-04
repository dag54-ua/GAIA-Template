import bleach
from uuid import UUID
from app.domain.repositories.incident_repository import IncidentRepository
from app.infrastructure.models.incident import Incident
from app.presentation.schemas.incident import CreateIncidentRequest

class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def create_incident(self, data: CreateIncidentRequest, owner_id: UUID) -> Incident:
        # XSS Sanitization
        sanitized_description = bleach.clean(data.description, tags=[], strip=True)
        sanitized_title = bleach.clean(data.title, tags=[], strip=True)

        incident = Incident(
            title=sanitized_title,
            description=sanitized_description,
            category=data.category,
            owner_id=owner_id
        )
        return await self.repository.create(incident)

    async def list_incidents(self, limit: int, offset: int) -> list[Incident]:
        return await self.repository.list(limit, offset)
