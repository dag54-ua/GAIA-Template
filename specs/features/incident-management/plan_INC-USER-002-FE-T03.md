# INC-USER-002-FE-T03 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-002-FE-T03**  
**Related user story**: **INC-USER-002** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-002-FE-T03`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the frontend feed to display reported incidents. Use a card layout/list optimized for reading.
- **Impacted entities/tables**: N/A.
- **Impacted services/modules**: `frontend/src/features/incidents/`, `frontend/src/api/`.
- **Impacted tests**: Component and E2E tests for the feed.

## 2) Scope
- **In scope**: 
  - `IncidentList` container.
  - `IncidentCard` presentational component.
  - Integration with `GET /api/v1/incidents`.
  - Loading skeleton state.
  - Empty state.
- **Out of scope**: 
  - Delete action (INC-USER-003).
  - Filtering/Sorting UI (v1 forces date desc).
- **Assumptions**: 
  - `Incident` type is defined in `types/`.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `frontend` container is running.

### 3.1 Test-first sequencing
1. **Defne E2E**: Update `tests/e2e/incidents.spec.ts` to assert that after creation, the new item appears in the list.
2. **Implement Hook**: `useIncidents` query hook.
3. **Implement Components**: `IncidentCard`, `IncidentList`.
4. **Integration**: Place list on `/incidents` page.
5. **Verify**: Run tests.

### 3.2 NFR hooks
- **Performance**: 
  - Use `Suspense` or explicit loading state to prevent layout shift (CLS).
  - Pagination strategy: infinite scroll or "Load More" (Simplest for v1: Load 50, standard scroll).
- **Brand & Visuals**: 
  - Card: `Card`, `CardHeader`, `CardTitle` from `shadcn`.
  - Badges: `Badge` component for Category.
  - Typography: `text-sm text-muted-foreground` for dates.
- **Observability**: 
  - Log error to console if fetch fails.

## 4) Atomic Task Breakdown

### Task 1: API Hook & Types
- **Purpose**: Fetch logic (INC-USER-001-FE-T03).
- **Prerequisites**: None.
- **Artifacts impacted**: `frontend/src/features/incidents/api/get-incidents.ts`, `frontend/src/types/start.ts` (Incident interface).
- **Test types**: Unit.
- **BDD Acceptance**:
  - **Given** the hook is called
  - **When** API returns data
  - **Then** it transforms dates to JS Date objects if needed.

### Task 2: Implement UI Components
- **Purpose**: Presentational layer.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `frontend/src/features/incidents/components/IncidentCard.tsx`, `frontend/src/features/incidents/components/IncidentList.tsx`.
- **Test types**: Component.
- **BDD Acceptance**:
  - **Given** a list of 3 incidents
  - **When** rendered
  - **Then** I see 3 cards with correct Titles and Category Badges.

### Task 3: Integration & Empty State
- **Purpose**: Final assembly.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `frontend/src/pages/incidents/IncidentsPage.tsx`.
- **Test types**: E2E.
- **BDD Acceptance**:
  - **Given** no incidents exist
  - **When** I visit the page
  - **Then** I see "No incidents found" message.
