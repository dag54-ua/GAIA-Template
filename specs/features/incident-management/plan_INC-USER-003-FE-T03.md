# INC-USER-003-FE-T03 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-003-FE-T03**  
**Related user story**: **INC-USER-003** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-003-FE-T03`.

---

## 1) Context & Objective
- **Ticket summary**: Add a UI action to allow users to delete their own incidents. It must show a confirmation dialog before proceeding.
- **Impacted entities/tables**: N/A (FE only).
- **Impacted services/modules**: `frontend/src/features/incidents/`, `IncidentCard.tsx`.
- **Impacted tests**: Component tests (interaction), E2E tests (delete flow).

## 2) Scope
- **In scope**: 
  - `DeleteIncidentDialog` component.
  - "Trash" icon button on `IncidentCard` (Conditional rendering).
  - `useDeleteIncident` hook connecting to `DELETE /api/v1/incidents/{id}`.
  - Optimistic update or Query Invalidation.
- **Out of scope**: 
  - Admin deletion.
  - Undo-delete (Toast with Undo is nice but out of scope for strict v1 unless strictly required, sticking to spec: "Confirmation dialog").
- **Assumptions**: 
  - `current_user` is available in frontend state to compare with `incident.owner_id`.
  - `AlertDialog` component available in `shadcn/ui`.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `frontend` container is running.

### 3.1 Test-first sequencing
1. **Define E2E**: Update `tests/e2e/incidents.spec.ts` to include a test where a user creates an incident, sees the delete button, clicks it, confirms, and validates it disappears.
2. **Implement Hook**: `useDeleteIncident` with invalidation.
3. **Implement UI**: Add button to Card and wire Dialog.
4. **Integration**: Verify flow.
5. **Verify**: Run tests.

### 3.2 NFR hooks
- **Security**: 
  - UI Hiding: If `user.id !== incident.owner_id`, return `null` for the delete button.
- **UX**: 
  - Destructive action warning (Red button in dialog).
  - Feedback: "Incident deleted" toast.
- **Accessibility**: 
  - Dialog focus management (Focus trap).
  - "Delete incident" aria-label on icon button.

## 4) Atomic Task Breakdown

### Task 1: API Hook & Dialog Component
- **Purpose**: logic and modal UI (INC-USER-003-FE-T03).
- **Prerequisites**: BE Endpoint ready (or mockable).
- **Artifacts impacted**: `frontend/src/features/incidents/api/delete-incident.ts`, `frontend/src/features/incidents/components/DeleteIncidentDialog.tsx`.
- **Test types**: Unit/Component.
- **BDD Acceptance**:
  - **Given** I am viewing the dialog
  - **When** I click Cancel
  - **Then** the dialog closes and no API call is made.

### Task 2: Integrate into Card
- **Purpose**: Expose action to user.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `frontend/src/features/incidents/components/IncidentCard.tsx`.
- **Test types**: Component.
- **BDD Acceptance**:
  - **Given** an incident owned by Me
  - **Then** I see the Trash icon.
  - **Given** an incident owned by Others
  - **Then** I DO NOT see the Trash icon.

### Task 3: E2E Verification
- **Purpose**: Verify full flow.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `frontend/tests/e2e/incidents.spec.ts`.
- **Test types**: E2E.
- **BDD Acceptance**:
  - **Given** I delete an incident
  - **When** I confirm
  - **Then** it disappears from the list immediately.
