from abc import ABC, abstractmethod
from typing import Optional
from app.infrastructure.models.incident import Incident

class IncidentRepository(ABC):
    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        pass

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[Incident]:
        pass
    
    @abstractmethod
    async def get_by_id(self, incident_id) -> Optional[Incident]:
        pass
    
    @abstractmethod
    async def soft_delete(self, incident: Incident) -> None:
        pass
