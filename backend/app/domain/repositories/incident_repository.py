from abc import ABC, abstractmethod
from typing import Optional
from app.infrastructure.models.incident import Incident

class IncidentRepository(ABC):
    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        pass
