# User Stories: Incident Management
`specs/features/incident-management/user-stories.md`

## 1. Introduction
**Feature:** Incident Management (`incident-management`)  
**Goals:** Centralize reporting, ensure visibility, and reduce duplicate reports.  
**Impact:** Enables neighbors to report and track community issues efficiently.

---

## 2. User Stories

### Story: Report Incident
**ID:** `INC-USER-001`  
**As a** Neighbor (`USER`),  
**I want to** report a maintenance issue or problem in the community,  
**So that** the administration and other neighbors are aware of it.

#### Acceptance Criteria

**Scenario 1: Successful creation**
- **Given** I am logged in as a Neighbor
- **When** I fill in the incident form with:
  - Title: "Broken light in hall"
  - Description: "The light near the elevator is flickering."
  - Category: "Maintenance"
- **And** I submit the form
- **Then** the system saves the incident
- **And** records the Creation Date automatically
- **And** I am redirected to the incident list
- **And** my new incident appears at the top.

**Scenario 2: Validation failure**
- **Given** I am on the creation form
- **When** I leave the Title or Description empty
- **And** I submit
- **Then** the system shows a "Required field" error
- **And** the incident is not created.

**Scenario 3: XSS Security Check (NFR)**
- **Given** a malicious user tries to submit a script tag in the Description
- **When** the incident is saved and viewed
- **Then** the script is NOT executed (it is sanitized or escaped).

---

### Story: View Community Incidents
**ID:** `INC-USER-002`  
**As a** Neighbor (`USER`),  
**I want to** view a list of all reported incidents,  
**So that** I can check if my issue has already been reported.

#### Acceptance Criteria

**Scenario 1: Chronological List**
- **Given** there are existing incidents
- **When** I access the main incident feed
- **Then** I see a list of incidents sorted by Date (newest first)
- **And** each item shows Title, Category (visual icon/badge), and Date.

**Scenario 2: Readability & Performance**
- **Given** the list contains 50 items
- **When** I load the page
- **Then** the list renders in less than 2 seconds (NFR-Perf)
- **And** the layout adapts to mobile or desktop screen size (Responsive).

---

### Story: Delete Own Incident
**ID:** `INC-USER-003`  
**As a** Neighbor (`USER`),  
**I want to** delete an incident I created,  
**So that** I can remove duplicate or erroneous reports.

#### Acceptance Criteria

**Scenario 1: Owner deletion**
- **Given** I see an incident created by me
- **When** I click the "Delete" action
- **And** I confirm the action
- **Then** the incident is removed from the list.

**Scenario 2: Access Control (Security)**
- **Given** I see an incident created by **another** neighbor
- **When** I look for the "Delete" action
- **Then** I do not see the delete button
- **And** if I try to force the API call, I receive a 403 Forbidden error.
