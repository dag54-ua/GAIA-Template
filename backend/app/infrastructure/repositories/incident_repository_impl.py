from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
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

    async def list(self, limit: int, offset: int) -> list[Incident]:
        query = select(Incident).order_by(desc(Incident.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())
