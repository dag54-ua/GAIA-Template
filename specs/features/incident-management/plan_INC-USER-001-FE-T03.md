# INC-USER-001-FE-T03 — Implementation Plan

**Source ticket**: `specs/features/incident-management/tickets.md` → **INC-USER-001-FE-T03**  
**Related user story**: **INC-USER-001** (from `specs/features/incident-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-03  
**Traceability**: tasks must reference `INC-USER-001-FE-T03`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the UI form to allow a neighbor to create a new incident. Connect it to the backend API.
- **Impacted entities/tables**: N/A (Frontend only).
- **Impacted services/modules**: `frontend/src/features/incidents/`, `frontend/src/api/`.
- **Impacted tests**: E2E test (Playwright) for creation flow.

## 2) Scope
- **In scope**: 
  - `CreateIncidentForm` component (Title, Category, Description).
  - Validation (Zod) + React Hook Form.
  - Integration with `POST /api/v1/incidents` via React Query hooks.
  - Redirect to list on success.
- **Out of scope**: 
  - Incident List (Next ticket).
  - Backend implementation.
- **Assumptions**: 
  - Backend API is ready or contract is defined.
  - UI Components (Button, Input, Select, Textarea) exist in `components/ui`.

## 3) Detailed Work Plan (TDD + BDD)
> **Container Check**: Ensure `frontend` container is running or Node environment is clean.

### 3.1 Test-first sequencing
1. **Define E2E Test**: Update/Create a Playwright test `tests/incidents/create-incident.spec.ts` that navigates to `/incidents/new`, fills the form, and asserts redirection/success message.
2. **Implement API Hook**: Create `useCreateIncident` mutation in `features/incidents/api/`.
3. **Implement Component**: Build the form with validation.
4. **Integration**: Wire the form to the hook.
5. **Verify**: Run E2E test.

### 3.2 NFR hooks
- **Accessibility**: 
  - Labels linked to inputs (`htmlFor`).
  - Error messages linked via `aria-describedby`.
  - Keyboard navigable.
- **Brand & Visuals**: 
  - Use `shadcn/ui` components (Input, Textarea, Button).
  - Spacing: `space-y-4`.
- **Connectivity**: 
  - Route: `/incidents/new` or a Modal triggered from `/incidents`. (Decision: New Page for simplicity or Modal if specified in design? Spec says "Route: /incidents/new or modal". Let's assume **New Page** for better deep linking/mobile friendliness in v1).

## 4) Atomic Task Breakdown

### Task 1: API Hook & Validation Schema
- **Purpose**: Prepare data layer (INC-USER-001-FE-T03).
- **Prerequisites**: None.
- **Artifacts impacted**: `frontend/src/features/incidents/api/create-incident.ts`, `frontend/src/features/incidents/schemas.ts`.
- **Test types**: Unit (Schema validation).
- **BDD Acceptance**:
  - **Given** an invalid input (empty title)
  - **When** I parse with Zod schema
  - **Then** it throws error.

### Task 2: Implement Create Form Component
- **Purpose**: UI implementation.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `frontend/src/features/incidents/components/CreateIncidentForm.tsx`.
- **Test types**: Component Test (Vitest).
- **BDD Acceptance**:
  - **Given** the form is rendered
  - **When** I click submit without typing
  - **Then** I see "Required" error messages.

### Task 3: Wire Page & E2E Test
- **Purpose**: Complete flow verification.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `frontend/src/pages/incidents/CreateIncidentPage.tsx`, `frontend/tests/e2e/incidents.spec.ts`.
- **Test types**: E2E (Playwright).
- **BDD Acceptance**:
  - **Given** I am on the create page
  - **When** I fill valid data and submit
  - **Then** I am redirected to the list page (mocked or real).
