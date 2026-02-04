from abc import ABC, abstractmethod
from typing import Optional
from app.infrastructure.models.incident import Incident

class IncidentRepository(ABC):
    @abstractmethod
    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        pass

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[Incident]:
        pass
