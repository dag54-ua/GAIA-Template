# INC-USER-001-BE-T02 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-001-BE-T02**  
**Related user story**: **INC-USER-001** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-001-BE-T02`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the API endpoint to create a new incident. Check for valid input and sanitize strings to prevent XSS.
- **Impacted entities/tables**: `incidents` (Insert).
- **Impacted services/modules**: `backend/app/presentation/routers/incidents.py`, `backend/app/application/services/incident_service.py`.
- **Impacted tests**: API integration tests (`POST /api/v1/incidents`).

## 2) Scope
- **In scope**: 
  - Pydantic DTOs (`CreateIncidentRequest`, `IncidentResponse`).
  - POST Endpoint implementation.
  - XSS Sanitization logic (using a library like `bleach` or similar).
  - Linking `owner_id` from the auth token.
- **Out of scope**: 
  - Database schema creation (handled in DB ticket).
  - Frontend integration.
- **Assumptions**: 
  - Authentication middleware injects `current_user`.
  - DB model `Incident` exists.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `backend` container is running.

### 3.1 Test-first sequencing
1. **Define Tests**: Create an API test that posts a new incident and expects 201 Created. Create another test passing HTML content in description and expecting it to be stripped in the response.
2. **Implement DTOs**: Define the contract in `presentation/schemas`.
3. **Implement Service**: Write the business logic (XSS cleaning, repository call) in `application`.
4. **Implement Router**: Wire up the endpoint in `presentation`.
5. **Verify**: Run tests.

### 3.2 NFR hooks
- **Security**: 
  - Rate limiting (standard global 100/min).
  - XSS Strip (Critical): `<script>` tags must be removed.
  - Auth: Only authenticated users can post.
- **Performance**: 
  - Single insert transaction.
- **Observability**: 
  - Log "Incident Created" with `incident_id` and `user_id`.

## 4) Atomic Task Breakdown

### Task 1: Define DTOs & Validation
- **Purpose**: Define input/output contracts (INC-USER-001-BE-T02).
- **Prerequisites**: None.
- **Artifacts impacted**: `backend/app/presentation/schemas/incident.py`.
- **Test types**: Unit (Pydantic validation).
- **BDD Acceptance**:
  - **Given** a create request with empty title
  - **When** I validate the schema
  - **Then** it raises a ValidationError.

### Task 2: Implement Incident Service & XSS Logic
- **Purpose**: Business logic layer (sanitization + db call).
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `backend/app/application/services/incident_service.py`.
- **Test types**: Unit.
- **BDD Acceptance**:
  - **Given** a description with `<script>alert('xss')</script>`
  - **When** I call `create_incident`
  - **Then** the stored description does NOT contain the script tag.

### Task 3: Implement POST Endpoint
- **Purpose**: Expose the functionality via HTTP.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `backend/app/presentation/routers/incidents.py`.
- **Test types**: API Integration.
- **BDD Acceptance**:
  - **Given** an authenticated user
  - **When** I POST to `/api/v1/incidents`
  - **Then** I receive a 201 status and the created incident data.
