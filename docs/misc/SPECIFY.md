# Specification

> High-level user & system requirements (SPEC-*). Source of truth for what and why. Drives PLAN and TASK layers.

## 1. Scope Statement
Deliver a modular CMS with content authoring, events & RSVP management, notifications, AI-assisted authoring, and site configuration—accessible via an authenticated web UI and stable REST APIs.

## 2. User Roles (Informational)
- **Admin** – Manages global settings, AI providers, modules, security posture.
- **Editor** – Creates & edits content, manages events, triggers notifications (where permitted).
- **Viewer** – (Future) Read-only access to published content / analytics snapshots.
- **Guest (Public)** – RSVP responses via invitation link.

## 3. Functional Requirements
Each requirement has an ID: SPEC-#. Acceptance criteria will be referenced by TASK-### entries.

### Content Management
- SPEC-1: System shall allow authenticated users (role ≥ editor) to create, update, list, fetch, and delete content records with unique slug per item.
- SPEC-2: System shall auto-generate a URL-safe slug from title; collisions resolved deterministically.
- SPEC-3: System shall store SEO metadata (title, description, keywords) with each content item.

### AI Assistance
- SPEC-4: System shall enable content generation or suggestions using a currently active AI provider.
- SPEC-5: Only one AI provider may be active at a time; switching provider deactivates others.
- SPEC-6: AI requests shall include request_id in logs for traceability (ties to observability principle).

### Modules
- SPEC-7: Admins can install, configure, activate, deactivate, and remove modules.
- SPEC-8: Module configuration supports encrypted API keys stored at rest.

### Site Settings
- SPEC-9: Admins can CRUD key/value settings and bulk update site configuration.
- SPEC-10: Sensitive setting values must be masked in read responses (show presence only / masked tail).

### Events & RSVPs
- SPEC-11: Authenticated users (role ≥ editor) can create & update events with start/end timestamps and RSVP configuration.
- SPEC-12: Guests can submit RSVP without authentication via invitation flow (public endpoint with controlled risk mitigations).
- SPEC-13: System tracks RSVP status changes and timestamps (invitation_sent, responded_at, reminders sent count).

### Notifications
- SPEC-14: System shall send invitation emails for events to a provided list of emails.
- SPEC-15: System shall send reminder emails based on configured days before event.
- SPEC-16: All outbound email attempts recorded as Communication entries with delivery status.

### Authentication & Authorization
- SPEC-17: Users can register and authenticate via username/password producing JWT access tokens.
- SPEC-18: System shall support role-based access, restricting admin-only actions (settings, provider creation, notifications dispatch) (enforced via dependency).
- SPEC-19: Refresh token rotation with revocation table (baseline implemented or scheduled via tasks) to enable logout/invalidation.

### Security & Compliance
- SPEC-20: Secrets and API keys never returned in plaintext after initial write.
- SPEC-21: All API responses include consistent error structure for business or validation errors.
- SPEC-22: System enforces structured logging (JSON) including request_id across request lifecycle.

### Observability & Metrics
- SPEC-23: The system emits request completion logs with path, method, status_code, and duration_ms.
- SPEC-24: Failures produce error logs including stack traces (non-HTTP exceptions) without leaking secrets.

### Performance & Scalability (Initial Targets)
- SPEC-25: Content list endpoint returns within < 300ms P95 for 1k records (baseline, single-node, warm cache scenario).
- SPEC-26: AI provider calls timeout (future enhancement) within configurable budget (default 30s) – placeholder acceptance.

### Governance & Traceability
- SPEC-27: Every merged code change references at least one TASK-### implementing SPEC-* or PLAN-*.
- SPEC-28: Governance docs (Constitution, Specification, Plan, Tasks, Enforcement) must exist in repository root and pass CI validation.

## 4. Non-Functional Requirements (Selected – expanded in NFR doc later)
| Requirement | Description | Trace |
|-------------|-------------|-------|
| Availability (initial) | Single-node dev environment; no HA guarantee | SPEC-25 (perf) |
| Security baseline | RBAC + secret masking + encrypted API keys | SPEC-10, SPEC-18, SPEC-20 |
| Observability core | Structured logs + request IDs | SPEC-22, SPEC-23 |

## 5. Out of Scope (Phase 1)
- Full-text search indexing
- Multi-tenancy / org isolation
- Webhook/event-driven plugin runtime
- Real-time websocket updates
- Soft delete/versioned content

## 6. Assumptions
- Single PostgreSQL instance; vertical scaling acceptable early stage.
- SMTP credentials valid and routable for notification testing.
- AI provider availability >= 99% (external dependency risk accepted initially).

## 7. Open Questions (to be resolved via ADR / Plan)
| ID | Question | Owner | Resolution Path |
|----|----------|-------|-----------------|
| OQ-1 | Should RSVP public endpoints adopt signed tokens vs numeric IDs? | TBD | ADR-0001 or security-focused ADR |
| OQ-2 | Which rate limiting strategy (Redis vs in-memory) for phase 1? | TBD | PLAN performance section |

## 8. Mapping Matrix (Spec → Plan → Tasks) (Will expand when Tasks file created)
Placeholder: After `TASKS.md` creation, this section will list for each SPEC the implementing TASK IDs.

## 9. Change Control
Changes require PR referencing updated SPEC IDs + linked TASK modifications; incompatible changes may need ADR if architectural impact.

## 10. Version & Log
Version: 0.1.0  
Created: 2025-09-20  
History: Initial extraction from existing code & component docs.

---
End of Specification.
