# Project Constitution

> Governing principles, decision hierarchy, and quality guardrails for Stitch CMS.

## 1. Purpose
Define durable, non-ephemeral rules that guide architectural, process, and quality decisions. Anything here is higher-order than transient tasks or implementation details.

## 2. Principles
Each principle gets a stable ID (CONST-P#) for traceability from specs, plan items, tasks, ADRs, and CI enforcement.

### CONST-P1: API First
All core capabilities must be exposed via stable, documented API endpoints before (or alongside) UI usage to enable automation, future CLI, and external integration.

### CONST-P2: Async & Non-Blocking Core
Backend I/O (DB, HTTP, SMTP, AI calls) should prefer async patterns to maximize throughput and reduce tail latency.

### CONST-P3: Extensibility by Abstraction
Subsystems (AI providers, modules, notifications) must define clear interface seams allowing future providers or plugins without large-scale refactors.

### CONST-P4: Separation of Concerns
Presentation/UX, domain logic, persistence, and integration boundaries remain decoupled. Cross-layer coupling requires justification via ADR.

### CONST-P5: Security & Privacy by Default
Secrets masked in responses, least-privilege role checks enforced, sensitive operations auditable. Adding a new surface must define authn/authz and data handling up front.

### CONST-P6: Spec-Driven Change Flow
All non-trivial features follow: Constitution → Specification (what/why) → Plan (how) → Tasks (units) → Implementation → Review. Skipping a phase requires explicit rationale recorded in PR.

### CONST-P7: Observability Required
Every deployed feature must emit minimally: structured logs with request_id + domain context; critical operations expose metrics or counters for health tracking.

### CONST-P8: Incremental Hardening
Security, performance, and resilience improvements can land iteratively but MUST create backlog tasks (TASK-###) referencing gaps rather than silent deferral.

### CONST-P9: Testable Units Only
No task is accepted without a deterministic success criterion (test, measurable output, or inspection checklist) aligning with at least one SPEC-* or PLAN-* reference.

### CONST-P10: Change Traceability
Every merged PR references at least one TASK-###; each TASK references at least one SPEC-* or PLAN-*; ADRs reference affected principles (CONST-P#) when modifying systemic choices.

### CONST-P11: Minimal Surface Area
Avoid premature endpoints, configuration flags, or data fields. Introduce only when tied to an accepted SPEC / PLAN item to reduce long-term maintenance load.

### CONST-P12: Fast Feedback & Small Batches
Prefer small, reviewable increments (≤ ~300 lines diff excluding generated code) to reduce cycle time & rollback blast radius.

## 3. Decision Hierarchy
1. Constitution (this document) – durable; changes require ADR + majority maintainer approval.
2. ADRs – architectural decisions; may supersede Plan entries; must cite impacted CONST-P#.
3. Plan (PLAN-#) – evolving architectural blueprint; updated via PR referencing relevant ADR or SPEC when structural shifts occur.
4. Specification (SPEC-#) – user-facing requirements; drives Plan evolution.
5. Tasks (TASK-###) – execution units implementing Plan/Spec.
6. Code – implementation detail; cannot silently diverge from higher layers.

## 4. Amendment Process
- Open PR modifying `CONSTITUTION.md` + new/updated ADR (status: Proposed → Accepted).
- Provide impact matrix: affected principles, rationale, migration considerations.
- Require: (a) all CI green, (b) at least 2 maintainer approvals.
- On merge: update any obsolete PLAN or SPEC references within same PR.

## 5. Compliance & Enforcement Hooks
- CI governance test validates presence of this file and uniqueness of CONST-P#.
- Lint rule (Python test) ensures every TASK line references valid SPEC/PLAN IDs.
- PR template prompts for TASK / SPEC / PLAN references.

## 6. Quality Bars (Linked to Principles)
| Area | Minimum Standard | Related Principles |
|------|------------------|--------------------|
| API Consistency | Versioned paths, explicit status codes | P1, P4, P10 |
| Security | Role checks + secret masking for sensitive fields | P5, P8 |
| Observability | Structured JSON logs + request_id | P7, P10 |
| Testing | Critical logic covered; tasks have verifiable criteria | P9, P6 |
| Architecture | Clear separation & abstractions for pluggable parts | P3, P4 |
| Change Control | PR links tasks/specs; ADR for systemic shifts | P6, P10 |

## 7. Roles & Responsibilities
| Role | Responsibilities |
|------|------------------|
| Maintainer | Approves ADRs, enforces Constitution, curates backlog |
| Contributor | Proposes SPEC/PLAN/TASK updates, implements tasks |
| Reviewer | Validates alignment w/ CONST-P*, checks traceability, flags drift |

## 8. Glossary
- **Principle (CONST-P#):** Governing rule – stable over time.
- **Specification (SPEC-#):** Describes user needs, acceptance criteria.
- **Plan Item (PLAN-#):** Architecture / system-level commitment.
- **Task (TASK-###):** Executable unit implementing higher layers.
- **ADR:** Architecture Decision Record justifying a significant irreversible or high-cost change.

## 9. Non-Negotiables Summary
If a proposed change violates a principle, it MUST: (a) justify via ADR, (b) update this constitution, or (c) be rejected.

## 10. Effective Date & Version
Version: 1.0.0  
Effective: 2025-09-20  
Change Log: Initial creation.

---
End of Constitution.
