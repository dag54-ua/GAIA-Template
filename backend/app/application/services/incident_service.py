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
    
    # [Feature: Incident Management] [Story: INC-USER-003] [Ticket: INC-USER-003-BE-T02]
    async def delete_incident(self, incident_id: UUID, current_user_id: UUID) -> None:
        from fastapi import HTTPException
        
        # Fetch the incident
        incident = await self.repository.get_by_id(incident_id)
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        # BOLA/IDOR Protection: Verify ownership
        if incident.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this incident")
        
        # Perform soft delete
        await self.repository.soft_delete(incident)
