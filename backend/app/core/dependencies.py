from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.infrastructure.repositories.incident_repository_impl import IncidentRepositoryImpl
from app.application.services.incident_service import IncidentService

def get_incident_service(db: AsyncSession = Depends(get_db)) -> IncidentService:
    repository = IncidentRepositoryImpl(db)
    return IncidentService(repository)

from uuid import UUID
from fastapi import Header, HTTPException

# Mock auth dependency for v1 until full auth is ready
async def get_current_user_id(x_user_id: str = Header(None)) -> UUID:
    if not x_user_id:
        # Fallback or error? For tests we might set this header. 
        # For now, let's assume it's passed or create a default dev user.
        # Strict mode: raise error
        raise HTTPException(status_code=401, detail="X-User-Id header required for dev auth")
    try:
        return UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID in X-User-Id")
