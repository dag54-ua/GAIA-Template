# Incident Management — Implementation Tickets
`specs/features/incident-management/tickets.md`

**Feature:** Incident Management (`incident-management`)  
**Core Dependencies:** `User Management` (Auth/Users table) for `owner_id`.

---

### Story: INC-USER-001 — Report Incident
**Source**: `user-stories.md`
**Key Scenarios**: Successful creation, Validation failure, XSS Security Check.

#### Tickets for INC-USER-001

1. - [x] **INC-USER-001-DB-T01 — Create Incidents Table** (2026-02-04)
   - **Type**: DB
   - **Description**: Create the database schema for incidents to store reports.
     - Table: `incidents`
     - Columns: `id` (UUID, PK), `title` (VarChar), `description` (Text), `category` (Enum: CLEANING, NOISE, MAINTENANCE, SECURITY), `created_at` (Timestamp, UTC), `updated_at` (Timestamp), `owner_id` (UUID, FK -> users.id).
   - **Deliverables**: Alembic migration script.
   - **Dependencies**: User table existing.

2. - [x] **INC-USER-001-BE-T02 — Create Incident Endpoint** (2026-02-04)
   - **Type**: BE
   - **Description**: Implement `POST /api/v1/incidents`.
     - Validate input using Pydantic V2 (`CreateIncidentRequest`).
     - **Security**: Sanitize `description` and `title` to strip HTML/Script tags (prevent XSS).
     - **Logic**: Associate `owner_id` from `current_user`.
     - **Tests**: Integration test verifying DB persistence and XSS stripping.
   - **Deliverables**: Router, Service, Schema, Tests.
   - **Dependencies**: INC-USER-001-DB-T01.

3. - [ ] **INC-USER-001-FE-T03 — Incident Creation Form**
   - **Type**: FE
   - **Description**: UI for reporintg a new incident.
     - Route: `/incidents/new` (or modal).
     - Fields: Title, Category (Select), Description (Textarea).
     - **Validation**: Zod schema (required fields, max length).
     - **State**: React Hook Form + useMutation.
   - **Deliverables**: `CreateIncidentForm` component, Zod schema, e2e test (Playwright).
   - **Dependencies**: INC-USER-001-BE-T02 (for contract).

---

### Story: INC-USER-002 — View Community Incidents
**Source**: `user-stories.md`
**Key Scenarios**: Chronological List, Readability & Performance.

#### Tickets for INC-USER-002

1. - [ ] **INC-USER-002-DB-T01 — Optimize Incidents Query**
   - **Type**: DB
   - **Description**: Ensure efficient retrieval for the chronological feed.
     - Add Index: `idx_incidents_created_at_desc` on `(created_at DESC)`.
   - **Deliverables**: Alembic migration for index (if not created in T01).
   - **Dependencies**: INC-USER-001-DB-T01.

2. - [ ] **INC-USER-002-BE-T02 — List Incidents Endpoint**
   - **Type**: BE
   - **Description**: Implement `GET /api/v1/incidents`.
     - **Pagination**: Implement limit/offset (default limit 50).
     - **Sort**: Fixed to `created_at` DESC.
     - **Response**: `IncidentResponse` DTO list. Include user alias if available (or just owner_id depending on privacy specs).
     - **Performance**: Ensure query doesn't N+1 on fetching owners (join user).
   - **Deliverables**: Endpoint, Tests.
   - **Dependencies**: INC-USER-002-DB-T01.

3. - [ ] **INC-USER-002-FE-T03 — Incident List Feed**
   - **Type**: FE
   - **Description**: Display the list of incidents.
     - Component: `IncidentList`.
     - **UI**: Card layout. Show Category badge (different colors), Title, Date (formatted relative e.g. "2 hours ago").
     - **State**: `useQuery` with key `['incidents']`.
     - **UX**: Loading skeleton per card. Empty state ("No incidents reported").
   - **Deliverables**: Components, Storybook/Preview (optional), Playwright test.
   - **Dependencies**: INC-USER-002-BE-T02.

---

### Story: INC-USER-003 — Delete Own Incident
**Source**: `user-stories.md`
**Key Scenarios**: Owner deletion, Access Control.

#### Tickets for INC-USER-003

1. - [ ] **INC-USER-003-DB-T01 — Soft Delete Support**
   - **Type**: DB
   - **Description**: Add support for soft deletion to maintain history/audit.
     - Add column: `deleted_at` (Timestamp, Nullable) to `incidents`.
   - **Deliverables**: Alembic migration.
   - **Dependencies**: INC-USER-002-DB-T01.

2. - [ ] **INC-USER-003-BE-T02 — Delete Incident Endpoint**
   - **Type**: BE
   - **Description**: Implement `DELETE /api/v1/incidents/{id}`.
     - **Security (Critical)**: Verify `incident.owner_id == current_user.id`. Return `403` if mismatch.
     - **Logic**: Perform soft delete (set `deleted_at = NOW()`).
     - **Query Update**: Ensure `GET /incidents` filters out `deleted_at IS NOT NULL`.
   - **Deliverables**: Endpoint updates, permission logic, ownership tests.
   - **Dependencies**: INC-USER-003-DB-T01.

3. - [ ] **INC-USER-003-FE-T03 — Delete Action UI**
   - **Type**: FE
   - **Description**: Add delete capability to the UI.
     - **Conditional Rendering**: Show "Trash" icon ONLY on cards where `incident.owner_id === current_user.id`.
     - **Interaction**: Confirmation dialog (Alert Dialog) before deletion.
     - **State**: `useMutation` for delete. Invalidate `['incidents']` query on success.
   - **Deliverables**: Update `IncidentCard` component, add `DeleteIncidentDialog`.
   - **Dependencies**: INC-USER-003-BE-T02.
