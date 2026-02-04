# INC-USER-002-BE-T02 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-002-BE-T02**  
**Related user story**: **INC-USER-002** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-002-BE-T02`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the API endpoint to list incidents with pagination, sorted by creation date.
- **Impacted entities/tables**: `incidents` (Select).
- **Impacted services/modules**: `backend/app/presentation/routers/incidents.py`, `backend/app/application/services/incident_service.py`.
- **Impacted tests**: API integration tests (`GET /api/v1/incidents`).

## 2) Scope
- **In scope**: 
  - `GET /api/v1/incidents` endpoint.
  - Query Parameters: `limit` (default 50), `offset` (default 0).
  - Sorting: Forced `created_at DESC`.
  - Response DTO: List of incidents.
- **Out of scope**: 
  - Filtering by category (future ticket).
  - Complex user expansion (User Alias/Name not yet in scope, just `owner_id`).
- **Assumptions**: 
  - Index from DB ticket exists for performance.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `backend` container is running.

### 3.1 Test-first sequencing
1. **Define Tests**: Create an API test that seeds 55 incidents and requests page 1 (limit 50) and page 2 (limit 50, offset 50), linking results to ensure correct ordering.
2. **Implement DTOs**: `IncidentResponse` (already defined in T01 or update here).
3. **Implement Service**: `list_incidents(limit, offset)` in service layer using repository.
4. **Implement Router**: `GET /` with query params.
5. **Verify**: Run tests.

### 3.2 NFR hooks
- **Performance**: 
  - **N+1 Check**: Ensure we are not performing 50 individual selects for associated data if we add user info later. For now, flat select is safe.
  - **Pagination**: Hard limit on `limit` param (max 100) to prevent DOS.

## 4) Atomic Task Breakdown

### Task 1: Update DTOs & Service
- **Purpose**: logic for listing (INC-USER-002-BE-T02).
- **Prerequisites**: None.
- **Artifacts impacted**: `backend/app/application/services/incident_service.py`.
- **Test types**: Unit.
- **BDD Acceptance**:
  - **Given** 3 incidents in DB
  - **When** I call `list_incidents(limit=2, offset=0)`
  - **Then** I receive only the 2 most recent ones.

### Task 2: Implement LIST Endpoint
- **Purpose**: API exposure.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `backend/app/presentation/routers/incidents.py`.
- **Test types**: API Integration.
- **BDD Acceptance**:
  - **Given** authenticated user
  - **When** I GET `/api/v1/incidents?limit=10`
  - **Then** I receive a JSON list of 10 items sorted by date descending.
