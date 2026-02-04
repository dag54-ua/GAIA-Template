import pytest
import uuid
from httpx import AsyncClient
from app.infrastructure.models.user import User
from app.infrastructure.models.incident import Incident
from app.core.database import get_db
from app.main import app
from sqlalchemy import text

@pytest.mark.asyncio
async def test_delete_incident_as_owner(async_client: AsyncClient, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    
    # Clean up
    await db_session.execute(text("TRUNCATE TABLE incidents CASCADE"))
    await db_session.execute(text("TRUNCATE TABLE users CASCADE"))
    await db_session.commit()
    
    # Setup: Create user and incident
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"owner_{user_id}@example.com")
    db_session.add(user)
    await db_session.commit()
    
    incident_id = uuid.uuid4()
    incident = Incident(
        id=incident_id,
        title="Test Incident",
        description="To be deleted",
        category="MAINTENANCE",
        owner_id=user_id
    )
    db_session.add(incident)
    await db_session.commit()
    
    headers = {"X-User-Id": str(user_id)}
    
    # Delete the incident
    response = await async_client.delete(f"/api/v1/incidents/{incident_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify it's soft deleted (not in list)
    list_response = await async_client.get("/api/v1/incidents", headers=headers)
    assert list_response.status_code == 200
    incidents = list_response.json()
    assert len(incidents) == 0
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_incident_not_owner(async_client: AsyncClient, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    
    # Clean up
    await db_session.execute(text("TRUNCATE TABLE incidents CASCADE"))
    await db_session.execute(text("TRUNCATE TABLE users CASCADE"))
    await db_session.commit()
    
    # Setup: Create two users
    owner_id = uuid.uuid4()
    other_user_id = uuid.uuid4()
    
    owner = User(id=owner_id, email=f"owner_{owner_id}@example.com")
    other_user = User(id=other_user_id, email=f"other_{other_user_id}@example.com")
    db_session.add_all([owner, other_user])
    await db_session.commit()
    
    # Create incident owned by owner
    incident_id = uuid.uuid4()
    incident = Incident(
        id=incident_id,
        title="Owner's Incident",
        description="Should not be deletable by others",
        category="SECURITY",
        owner_id=owner_id
    )
    db_session.add(incident)
    await db_session.commit()
    
    # Try to delete as other user
    headers = {"X-User-Id": str(other_user_id)}
    response = await async_client.delete(f"/api/v1/incidents/{incident_id}", headers=headers)
    assert response.status_code == 403
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_list_excludes_deleted_incidents(async_client: AsyncClient, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    
    # Clean up
    await db_session.execute(text("TRUNCATE TABLE incidents CASCADE"))
    await db_session.execute(text("TRUNCATE TABLE users CASCADE"))
    await db_session.commit()
    
    # Setup
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"test_{user_id}@example.com")
    db_session.add(user)
    await db_session.commit()
    
    # Create two incidents
    incident1_id = uuid.uuid4()
    incident1 = Incident(
        id=incident1_id,
        title="Active Incident",
        description="Should appear",
        category="CLEANING",
        owner_id=user_id
    )
    
    incident2_id = uuid.uuid4()
    incident2 = Incident(
        id=incident2_id,
        title="Deleted Incident",
        description="Should not appear",
        category="NOISE",
        owner_id=user_id
    )
    
    db_session.add_all([incident1, incident2])
    await db_session.commit()
    
    headers = {"X-User-Id": str(user_id)}
    
    # Delete incident2
    await async_client.delete(f"/api/v1/incidents/{incident2_id}", headers=headers)
    
    # List should only show incident1
    list_response = await async_client.get("/api/v1/incidents", headers=headers)
    assert list_response.status_code == 200
    incidents = list_response.json()
    assert len(incidents) == 1
    assert incidents[0]["id"] == str(incident1_id)
    
    app.dependency_overrides.clear()
