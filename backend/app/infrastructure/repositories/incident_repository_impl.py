from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repositories.incident_repository import IncidentRepository
from app.infrastructure.models.incident import Incident

class IncidentRepositoryImpl(IncidentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, incident: Incident) -> Incident:
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident
