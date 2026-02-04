# INC-USER-003-DB-T01 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-003-DB-T01**  
**Related user story**: **INC-USER-003** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-003-DB-T01`.

---

## 1) Context & Objective
- **Ticket summary**: Add support for "soft deletion" to the `incidents` table. This allows us to hide incidents without losing data for audit purposes.
- **Impacted entities/tables**: `incidents`.
- **Impacted services/modules**: Alembic migrations.
- **Impacted tests**: DB integration tests to verify column existence.

## 2) Scope
- **In scope**: 
  - Add `deleted_at` timestamp column (Nullable).
  - Alembic migration.
- **Out of scope**: 
  - Updating queries to filter by `deleted_at` (BE ticket).
  - Deletion API logic.
- **Assumptions**: 
  - `incidents` table exists.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure DB container is running.

### 3.1 Test-first sequencing
1. **Define Test**: Test that `deleted_at` column exists and defaults to NULL.
2. **Implement Migration**: Mutation script.
3. **Apply**: `alembic upgrade head`.
4. **Verify**: Run valid SQL or inspect schema.

### 3.2 NFR hooks
- **Audit**: Soft delete preserves the record.
- **Performance**: N/A for adding a nullable column.

## 4) Atomic Task Breakdown

### Task 1: Generate Soft Delete Migration
- **Purpose**: Add column (INC-USER-003-DB-T01).
- **Prerequisites**: `incidents` table exists.
- **Artifacts impacted**: `backend/alembic/versions/xxxx_add_deleted_at_to_incidents.py`.
- **Test types**: Integration (Migration verify).
- **BDD Acceptance**:
  - **Given** the incidents table
  - **When** I apply the migration
  - **Then** the `deleted_at` column is present and NULLABLE.
