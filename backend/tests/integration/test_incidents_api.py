import pytest
import uuid
from httpx import AsyncClient
from app.infrastructure.models.user import User
from app.infrastructure.models.incident import IncidentCategory
from app.core.database import get_db
from app.main import app

@pytest.mark.asyncio
async def test_create_incident_api_success(async_client: AsyncClient, db_session):
    # Override dependency
    app.dependency_overrides[get_db] = lambda: db_session
    
    # Setup: Create user in DB to satisfy FK
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"api_test_{user_id}@example.com")
    db_session.add(user)
    await db_session.commit()

    payload = {
        "title": "Broken Streetlight",
        "description": "The light is flickering constantly.",
        "category": "MAINTENANCE"
    }
    
    headers = {"X-User-Id": str(user_id)}

    response = await async_client.post("/api/v1/incidents", json=payload, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["owner_id"] == str(user_id)
    assert "id" in data
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_incident_xss_sanitization(async_client: AsyncClient, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    
    # Setup user
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"xss_test_{user_id}@example.com")
    db_session.add(user)
    await db_session.commit()

    payload = {
        "title": "Normal Title",
        "description": "This is <script>alert('bad')</script> harmless.",
        "category": "SECURITY"
    }
    headers = {"X-User-Id": str(user_id)}

    response = await async_client.post("/api/v1/incidents", json=payload, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    # Check that script tag is gone
    assert "<script>" not in data["description"]
    assert "alert('bad')" in data["description"]
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_incident_unauthorized(async_client: AsyncClient, db_session):
     # Even for 401 we need dependency override if it's evaluated?
     # Auth dep is evaluated maybe before DB, but to be safe:
    app.dependency_overrides[get_db] = lambda: db_session
    
    payload = {
        "title": "Secret Incident",
        "description": "Shhh",
        "category": "NOISE"
    }
    # No header
    response = await async_client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 401
    
    app.dependency_overrides.clear()
