# Documentation & Rules Inventory

> Snapshot inventory of existing markdown artifacts and their alignment with Spec Kit phases and governance domains.

Generated: 2025-09-19

## 1. Inventory Table

| File | Present? | Primary Purpose | Audience | Currency (Fresh/Stale) | Overlaps / Redundancy | Spec Kit Phase Mapping | Cross-Cutting Domains |
|------|----------|-----------------|----------|------------------------|-----------------------|------------------------|-----------------------|
| `README.md` | Yes | External-facing repo introduction (currently auto-synced deployment info) | All contributors, external viewers | Fresh (auto-generated) | Lacks internal architecture; overlaps minimally | None (pre-phase context) | Deployment, Operations |
| `components.md` | Yes | Comprehensive architecture & component catalog | Developers, reviewers | Fresh (recently extended) | Contains roadmap pieces, complexity, security suggestions (may fragment with future PLAN doc) | Mix: Specify (problem/context), Plan (architecture), Tasks seeds (roadmap list) | Architecture, Security, Observability |
| `backend_api_catalog.md` | Yes | Endpoint-level backend reference + recommendations | Backend devs, API consumers | Fresh | Some duplication with sections 4–11 in `components.md` | Plan (technical surface), Tasks seeds (improvement checklist) | Security, Architecture, Quality |
| `project-rules.md` | No (referenced) | (Expected) Project-wide governance & principles | All contributors | Missing | Content currently diffused across other docs | Constitution (intended) | Governance |
| `repository-rules.md` | No (referenced) | (Expected) Contribution workflow, branching, commit conventions | Contributors | Missing | Would overlap future CONTRIBUTING.md | Plan → Implement support | Workflow, Automation |
| `agent-guidelines.md` | No (referenced) | (Expected) AI agent usage, boundaries, prompts structure | Developers using AI | Missing | Some implicit patterns in discussions | Cross-cutting (applies to all phases) | AI Collaboration |
| `styling-guide.md` | No (referenced) | (Expected) Frontend component & styling conventions | Frontend devs | Missing | Could merge into design-system docs later | Implement (execution standards) | UI Consistency |
| `architecture-overview.md` | No (referenced) | (Expected) High-level system view (now part of `components.md`) | New engineers | Superseded | Redundant with `components.md` sections 1–3 | Specify/Plan (already captured) | Architecture |
| `CONSTITUTION.md` | No | Governing principles & quality bars | All contributors | Missing | N/A | Constitution | Governance |
| `SPECIFY.md` | No | User goals, problem statements, acceptance criteria | Product + Eng | Missing | N/A | Specify | Product Requirements |
| `PLAN.md` | No | Technical decisions, ADR index, data strategies | Engineers/Leads | Missing | N/A | Plan | Architecture, Data |
| `TASKS.md` | No | Traceable task breakdown w/ IDs | Engineers | Missing | N/A | Tasks | Execution |
| `ENFORCEMENT.md` | No | Tooling gates & automation policies | Maintainers | Missing | N/A | Implement (quality gating) | Automation, Quality |
| `ADR/*` | No | Architecture Decision Records | Engineers/Stakeholders | Missing | Some decisions implicit only | Plan | Architecture, Governance |
| `RISK_REGISTER.md` | No | Catalog of risks & mitigations | Leads | Missing | Risks sprinkled in notes only | Plan → Tasks | Risk Management |
| `NON_FUNCTIONAL_REQUIREMENTS.md` | No | Performance, security, reliability targets | All contributors | Missing | Scattered hints only | Specify/Plan | Quality Attributes |
| `TEST_STRATEGY.md` | No | Testing levels, coverage targets, tools | QA/Devs | Missing | Suggested in docs only | Plan → Implement | Quality |

## 2. Key Observations
- Core internal knowledge is concentrated in `components.md` and `backend_api_catalog.md`, currently mixing conceptual, structural, and roadmap content.
- Foundational governance layers (Constitution, Spec, Plan, Tasks) are absent as discrete artifacts.
- Improvement roadmap items lack traceability IDs; converting them will enable progress tracking & automation.
- README is deployment-centric—should link into the forthcoming Constitution/Spec for discoverability.

## 3. Immediate Recommendations (Phase 0 → Phase 1)
1. Carve out new `CONSTITUTION.md` (principles, decision hierarchy, quality bars) by extracting stable sections from `components.md` (avoid duplication—leave pointers).
2. Introduce `PLAN.md` skeleton: system context diagram reference, service boundaries, initial ADR index, migration approach stub.
3. Create `SPECIFY.md` focusing on user roles (author, event organizer, site admin), primary use cases, acceptance criteria for current MVP scope.
4. Assign IDs (SPEC-#, PLAN-#, TASK-#) and annotate existing roadmap bullets accordingly.
5. Add a minimal `TASKS.md` converting the improvement backlog into atomic, testable items with phase labeling (Security, Observability, Performance, DX).
6. Prepare `ENFORCEMENT.md` stub enumerating intended gates—populate incrementally as CI config lands.

## 4. Proposed Extraction Plan
| Source Section (`components.md`) | Destination | Action |
|----------------------------------|------------|--------|
| 1. High-Level Overview (vision) | SPECIFY.md | Copy (light edit to user/problem framing) |
| Core Pillars | CONSTITUTION.md | Move (normalize as principles) |
| 2–3 Backend/Frontend Components | PLAN.md | Reference (keep canonical in components; link) |
| 5–10 AI/Notif/Module/Scalability | PLAN.md | Summarize; leave detailed tables in components | 
| 11 Suggested Next Steps | TASKS.md | Transform into TASK-# list |
| 9 Security Model (table) | PLAN.md (security baseline) | Copy & reformat with target states |
| 10 Scalability & Performance | NON_FUNCTIONAL_REQUIREMENTS.md | Extract target metrics |
| 15.5 Opportunities & Evolution | TASKS.md / PLAN.md | Split: strategic vs tactical |

## 5. Pending Artifacts to Add (Next Steps)
- `CONSTITUTION.md`
- `SPECIFY.md`
- `PLAN.md`
- `TASKS.md`
- `ENFORCEMENT.md`
- `ADR/0001-auth-strategy.md`
- `ADR/0002-ai-provider-architecture.md`
- `NON_FUNCTIONAL_REQUIREMENTS.md`
- `TEST_STRATEGY.md`
- `RISK_REGISTER.md`

## 6. Rationale for Creating This Inventory File
Centralizing the current state enables:
- Clear gap visualization without rereading large narrative docs.
- Deterministic extraction plan (avoids copy-paste drift and duplication).
- A staging ground to incrementally commit governance artifacts—reviewers can diff strategy evolution.
- Foundation for automation (a script can later validate presence & freshness timestamps of required governance docs).

## 7. Quality Scoring (Subjective Initial Pass)
| Dimension | Current Maturity (1–5) | Notes |
|-----------|------------------------|-------|
| Architecture Clarity | 4 | Rich detail present. |
| Governance Formalization | 1 | No constitution/spec documents yet. |
| Traceability | 1 | No ID system; tasks not linked to specs. |
| Security Policy Formalization | 2 | Risks noted but not codified. |
| Testing Strategy | 1 | Only recommendations. |
| Observability Strategy | 1 | Blueprint suggested, no artifact. |
| Documentation Modularity | 2 | Monolithic `components.md` doing many jobs. |

## 8. Acceptance Criteria to Mark Inventory Complete
- All existing and referenced-but-missing docs enumerated (DONE in this file).
- Each mapped to intended Spec Kit phase (DONE in table).
- Extraction plan defined (DONE Section 4).
- List of new artifacts to create captured (DONE Section 5).

## 9. Next Action
Proceed to build the mapping matrix (using this table as backbone) and then formal gap analysis expanding on maturity scoring deficiencies.

---
(End of Inventory)
