# INC-USER-002-DB-T01 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-002-DB-T01**  
**Related user story**: **INC-USER-002** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-002-DB-T01`.

---

## 1) Context & Objective
- **Ticket summary**: Optimize the database for retrieving the list of incidents in reverse chronological order.
- **Impacted entities/tables**: `incidents`.
- **Impacted services/modules**: Alembic migrations.
- **Impacted tests**: N/A (Performance optimization, verified by inspecting schema).

## 2) Scope
- **In scope**: 
  - Adding a B-Tree index on `created_at DESC` for the `incidents` table.
  - Alembic migration.
- **Out of scope**: 
  - Any code changes in backend/frontend.
- **Assumptions**: 
  - `incidents` table exists (from previous ticket).

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure DB container is running.

### 3.1 Test-first sequencing
1. **Define Verification Steps**: Since this is an index, we verify by checking the Postgres schema metadata `\d incidents` or `pg_indexes`.
2. **Implement Migration**: Create migration script adding the index.
3. **Apply**: Run `alembic upgrade head`.
4. **Verify**: Check database for index existence.

### 3.2 NFR hooks
- **Performance**: 
  - Index `idx_incidents_created_at_desc` ensures `ORDER BY created_at DESC LIMIT 50` is efficient (Index Scan instead of Seq Scan).

## 4) Atomic Task Breakdown

### Task 1: Generate Index Migration
- **Purpose**: Create the index (INC-USER-002-DB-T01).
- **Prerequisites**: Table `incidents` exists.
- **Artifacts impacted**: `backend/alembic/versions/xxxx_add_index_incidents_created_at.py`.
- **Test types**: Integration (Migration verify).
- **BDD Acceptance**:
  - **Given** the database
  - **When** I apply the migration
  - **Then** the index `idx_incidents_created_at_desc` exists on table `incidents`.
