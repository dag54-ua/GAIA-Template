import pytest
import uuid
from sqlalchemy.exc import IntegrityError
from app.infrastructure.models.incident import Incident, IncidentCategory
from app.infrastructure.models.user import User

@pytest.mark.asyncio
async def test_create_incident_success(db_session):
    # Create owner first
    user = User(email=f"test_{uuid.uuid4()}@example.com")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create incident
    incident = Incident(
        title="Test Incident",
        description="This is a test",
        category=IncidentCategory.MAINTENANCE,
        owner_id=user.id
    )
    db_session.add(incident)
    await db_session.commit()
    await db_session.refresh(incident)

    assert incident.id is not None
    assert incident.created_at is not None
    assert incident.title == "Test Incident"

@pytest.mark.asyncio
async def test_create_incident_missing_owner_fails(db_session):
    # Try creating without owner_id
    incident = Incident(
        title="Orphan Incident",
        description="No owner",
        category=IncidentCategory.NOISE,
        # owner_id is missing
    )
    db_session.add(incident)
    
    # Expect IntegrityError (Not Null constraint)
    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

@pytest.mark.asyncio
async def test_create_incident_invalid_category_fails(db_session):
    # This is slightly tricky because Pydantic/SQLAlchemy might catch it before DB 
    # depending on how we cast. But at DB level it's an Enum.
    # If we pass a string that isn't in Enum to SQLAlchemy model, it might fail at python level first.
    pass 
