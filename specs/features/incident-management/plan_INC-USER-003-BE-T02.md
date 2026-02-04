# INC-USER-003-BE-T02 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-003-BE-T02**  
**Related user story**: **INC-USER-003** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-003-BE-T02`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the `DELETE` endpoint. It must verify that the requester is the owner of the incident. If so, perform a "soft delete" (timestamping `deleted_at`). Also, ensure the List endpoint filters out deleted items.
- **Impacted entities/tables**: `incidents` (Update).
- **Impacted services/modules**: `incident_service.py`, `routers/incidents.py`.
- **Impacted tests**: API tests for deletion outcomes and permission denied scenarios.

## 2) Scope
- **In scope**: 
  - `DELETE /api/v1/incidents/{id}` endpoint.
  - Business logic: Check `incident.owner_id == current_user.id`.
  - Update `list_incidents` query to filter `deleted_at IS NULL`.
- **Out of scope**: 
  - Admin deletion (future).
  - Permanent delete.
- **Assumptions**: 
  - `deleted_at` column exists (from DB T01).
  - Auth context is available.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `backend` container is running.

### 3.1 Test-first sequencing
1. **Define Tests**: 
   - Test A: User A deletes User A's incident -> 204 No Content. Retrieve it -> 404 or missing from list.
   - Test B: User B tries to delete User A's incident -> 403 Forbidden.
2. **Refactor List Query**: Update the service/repo to default to `deleted_at IS NULL`.
3. **Implement Delete**: Add logic to Service and Router.
4. **Verify**: Run tests.

### 3.2 NFR hooks
- **Security**: 
  - **BOLA/IDOR protection**: Explicit check `if incident.owner_id != user.id: raise Forbidden`.
- **Audit**: Data remains in DB (soft delete).

## 4) Atomic Task Breakdown

### Task 1: Update List Logic (Filter Deleted)
- **Purpose**: Ensure we don't return deleted items (INC-USER-003-BE-T02).
- **Prerequisites**: DB Column exists.
- **Artifacts impacted**: `backend/app/application/services/incident_service.py` (or repository).
- **Test types**: Unit/Integration.
- **BDD Acceptance**:
  - **Given** one active incident and one soft-deleted incident
  - **When** I call `list_incidents()`
  - **Then** I receive only the active one.

### Task 2: Implement Delete Logic & Security
- **Purpose**: Permission check and soft delete.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `backend/app/application/services/incident_service.py`.
- **Test types**: Unit.
- **BDD Acceptance**:
  - **Given** an incident owned by User A
  - **When** User B calls delete
  - **Then** it raises `PermissionDenied` (403).
  - **When** User A calls delete
  - **Then** `incident.deleted_at` is updated to current time.

### Task 3: Implement DELETE Endpoint
- **Purpose**: API exposure.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `backend/app/presentation/routers/incidents.py`.
- **Test types**: API Integration.
- **BDD Acceptance**:
  - **Given** I am owner of incident #123
  - **When** I DELETE `/api/v1/incidents/123`
  - **Then** I get 204.
