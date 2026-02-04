import pytest
import uuid
import asyncio
from datetime import timedelta, datetime, timezone
from httpx import AsyncClient
from app.infrastructure.models.user import User
from app.infrastructure.models.incident import Incident, IncidentCategory
from app.core.database import get_db
from app.main import app

@pytest.mark.asyncio
async def test_list_incidents_pagination_and_sorting(async_client: AsyncClient, db_session):
    # Override dependency
    app.dependency_overrides[get_db] = lambda: db_session

    from sqlalchemy import text
    await db_session.execute(text("TRUNCATE TABLE incidents CASCADE"))
    await db_session.execute(text("TRUNCATE TABLE users CASCADE"))
    await db_session.commit()

    # Setup: Create user
    user_id = uuid.uuid4()
    user = User(id=user_id, email=f"list_test_{user_id}@example.com")
    db_session.add(user)
    await db_session.commit()

    # Setup: Create 15 incidents with different timestamps
    # To ensure stable sort order test, we space them out.
    base_time = datetime.now(timezone.utc)
    incidents = []
    for i in range(15):
        inc = Incident(
            id=uuid.uuid4(),
            title=f"Incident {i}",
            description=f"Description {i}",
            category="MAINTENANCE",
            owner_id=user_id,
            created_at=base_time - timedelta(minutes=i) # i=0 is newest, i=14 is oldest
        )
        incidents.append(inc)
    
    db_session.add_all(incidents)
    await db_session.commit()

    headers = {"X-User-Id": str(user_id)}

    # 1. Fetch Page 1 (Limit 10)
    response = await async_client.get("/api/v1/incidents?limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Sort check: Newest first. 
    # Index 0 should be "Incident 0" (created_at = base_time)
    assert data[0]["title"] == "Incident 0"
    # Index 9 should be "Incident 9"
    assert data[9]["title"] == "Incident 9"

    # 2. Fetch Page 2 (Limit 10, Offset 10) -> Should return remaining 5
    response_p2 = await async_client.get("/api/v1/incidents?limit=10&offset=10", headers=headers)
    assert response_p2.status_code == 200
    data_p2 = response_p2.json()
    assert len(data_p2) == 5
    assert data_p2[0]["title"] == "Incident 10"
    assert data_p2[4]["title"] == "Incident 14"

    # 3. Default params check (limit 50, offset 0)
    response_def = await async_client.get("/api/v1/incidents", headers=headers)
    assert response_def.status_code == 200
    assert len(response_def.json()) == 15

    app.dependency_overrides.clear()
