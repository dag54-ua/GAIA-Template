# INC-USER-001-DB-T01 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-001-DB-T01**  
**Related user story**: **INC-USER-001** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: All tasks must include inline references to `INC-USER-001-DB-T01` and `INC-USER-001`.

---

## 1) Context & Objective
- **Ticket summary**: Define and implement the database schema for the `incidents` table to allow neighbors to report cleaning, noise, and maintenance issues.
- **Impacted entities/tables**: `incidents` (New), references `users`.
- **Impacted services/modules**: `backend/app/infrastructure/models.py` (or dedicated module), Alembic migrations.
- **Impacted tests**: DB integration tests ensuring table creation and constraint enforcement.

## 2) Scope
- **In scope**: 
  - SQLAlchemy model Definition for `Incident`.
  - Enum definition for `IncidentCategory`.
  - Foreign Key to `users.id`.
  - Alembic migration script.
- **Out of scope**: 
  - API Endpoints (POST/GET).
  - Frontend forms.
  - Seeding data (unless needed for tests).
- **Assumptions**: 
  - `users` table exists (or will be mocked/created in a prior migration within the same branch if missing).
  - Backend project structure follows `techstack-backend.md`.
- **Open questions**: 
  - None.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure a distinct `docker-compose.yml` exists. Verify `backend` service is healthy.

### 3.1 Test-first sequencing
1. **Define Tests**: Create a test that attempts to insert an incident record and expects success, and one that fails on missing required fields or invalid category.
2. **Implement Model**: Write the SQLAlchemy model in `infrastructure`.
3. **Migration**: Auto-generate migration with Alembic.
4. **Verify**: Apply migration and run the test.

### 3.2 NFR hooks
- **Security**: 
  - `owner_id` is mandatory (Constraint).
  - PII: Table does not store sensitive user data directly, only FK.
- **Performance**: 
  - Primary Key `id` (UUID).
  - `created_at` for sorting (Index to be added in future ticket or now if specified).
- **Observability**: None at DB level.

## 4) Atomic Task Breakdown

### Task 1: Define Incident Model
- **Purpose**: Define the structure of the `incidents` table in code (INC-USER-001).
- **Prerequisites**: Backend structure exists.
- **Artifacts impacted**: `backend/app/domain/models.py` (if shared) or `backend/app/infrastructure/database/models/incident.py`.
- **Test types**: Unit (Model instantiation).
- **BDD Acceptance**:
  - **Given** the Incident model
  - **When** I define a valid incident dictionary
  - **Then** it validates the Enum category.

### Task 2: Generate and Apply Migration
- **Purpose**: Materialize the table in the database (INC-USER-001-DB-T01).
- **Prerequisites**: Task 1 complete, DB container running.
- **Artifacts impacted**: `backend/alembic/versions/xxxx_create_incidents_table.py`.
- **Test types**: Integration (Migration up/down).
- **BDD Acceptance**:
  - **Given** a clean database
  - **When** I apply the migration
  - **Then** the `incidents` table exists in PostgreSQL.

### Task 3: Verify Persistence Constraints
- **Purpose**: Ensure DB constraints (FK, Not Null) are working.
- **Prerequisites**: Task 2 complete.
- **Artifacts impacted**: `backend/tests/integration/test_incidents_db.py`.
- **Test types**: Integration using Pytest.
- **BDD Acceptance**:
  - **Given** the `incidents` table
  - **When** I insert an incident without an `owner_id`
  - **Then** the database raises an IntegrityError.
