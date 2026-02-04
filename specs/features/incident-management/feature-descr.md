# Feature: Incident Management
`specs/features/incident-management/feature-descr.md`

## 0) Feature Name & Summary
**Feature Name:** Incident Management

**Executive Summary (3–5 lines):**  
- **Problem:** Neighbors currently report issues via unstructured channels (WhatsApp, email), causing duplication and lack of tracking.  
- **Opportunity:** Centralize incident reporting in a unified web platform to ensure visibility and traceability.  
- **Expected Outcome:** Increased transparency, reduced duplicates, and a clearer understanding of community issues for all neighbors.

**Fit with Vision / Product Goal:**  
This feature is the core value proposition of the application ("MVP"), directly addressing the goal of facilitating communication and increasing visibility of neighborhood problems.

---

## 1) Description of the feature 
The "Incident Management" feature allows registered neighbors to report community issues (cleaning, noise, maintenance) through a simple web form. Usage is transparent: any neighbor can see all reported incidents in a chronological list. To maintain control without complexity, users can only delete incidents they created themselves. The design focuses on simplicity and readability on both desktop and mobile devices.

---

## 2) Users/Roles & Impacted Personas

| Role/Persona | Key Objectives | Tasks / Jobs-to-be-done | Current Pain | Stakeholders |
|---|---|---|---|---|
| `Neighbor` | Report and track issues | Create incident, View community list, Delete own error | No way to know if an issue is already reported; messages get lost in chat groups | Board Members (future Admin) |

---

## 3) Problem / Opportunity Statement
**Context:** Residential community with common areas and shared maintenance needs.  
**Problem Statement:** Our **User (Neighbor)** experiences **frustration and uncertainty** when **encountering a maintenance issue**, which causes **duplicate reports and perception of inaction**.  
**Why Now:** The association wants to modernize its management and reduce the noise in informal channels immediately.

---

## 4) Objectives & Business Outcomes

| Objective / Outcome | KPI / Metric | Baseline | Target | Time Horizon | Measurement Method |
|---|---|---|---|---|---|
| Centralize reporting | # of incidents created in App | 0 | 10+ / week | Month 1 | DB Count |
| Reduce informal noise | % reduction in WhatsApp reports | N/A | 50% | Month 2 | Survey / Feedback |
| Active Participation | % of neighbors logging in | 0 | 30% | Month 3 | Analytics |

---

## 5) Scope (In/Out)
**In scope:**  
- **Create Incident:** Form with Title, Description, Category (Enums), Auto-date.  
- **List Incidents:** Public feed of all active incidents (sorted by date desc).  
- **Delete Incident:** Action available only to the creator of the incident.  
- **Visual Categories:** Distinct visual indicators for different types (Cleanliness, Noise, etc.).

**Out of scope (to prevent scope creep):**  
- **Edit Incident:** (Only delete and recreate allowed in v1).  
- **Comments/Threads:** No discussion on incidents yet.  
- **Status Workflow:** All incidents are "Open/Reported" by default; no "In Progress"/"Done" separation yet.  
- **Admin Role:** No special moderator privileges in this slice.  
- **Image Uploads:** Text-only for v1.

**Key Assumptions:**  
- Users are trusted to delete only if resolved or erroneous (honor system for v1).  
- All neighbors are authenticated before accessing the app.

**Dependencies / Blockers:**  
- Auth system (User Management) must provide `current_user` context.

---

## 6) Non-Functional Requirements (NFRs)

### 6.1 Security & Privacy
- **Access Control:** All endpoints protected by authentication.
- **Ownership:** `DELETE /incidents/{id}` must verify `resource.owner_id == current_user.id`.
- **Input Validation:** Strict sanitization of Title/Description to prevent XSS.
- **PII:** No personal data required in incident description (users advised not to post PII).

### 6.2 Performance
- **Load Time:** Main feed renders in < 1s (P95).
- **Pagination:** Backend should support pagination or limit (e.g., last 50) to prevent payload explosion, though Frontend may use infinite scroll or simple load.

### 6.3 Availability & Reliability
- **Uptime:** Standard web app availability (99%).
- **Error Handling:** Graceful error messages if creation fails.

### 6.4 Accessibility (a11y) & Internationalization (i18n)
- **Language:** UI in Spanish (Castilian).
- **A11y:** Semantic HTML, ARIA labels for category icons, high contrast text.

### 6.5 Observability
- **Logs:** Structured logs for "Incident Created" and "Incident Deleted" events with User ID.
