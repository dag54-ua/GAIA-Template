from fastapi import APIRouter, Depends, status
from uuid import UUID
from app.presentation.schemas.incident import CreateIncidentRequest, IncidentResponse
from app.application.services.incident_service import IncidentService
from app.core.dependencies import get_incident_service, get_current_user_id

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(
    request: CreateIncidentRequest,
    service: IncidentService = Depends(get_incident_service),
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await service.create_incident(request, current_user_id)
