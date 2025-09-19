# Project Components Documentation

> Stitch CMS – Architectural & Component Reference

## 1. High-Level Overview
Stitch CMS is a modular, AI-augmented content and event management platform built with a **FastAPI** backend and a **Next.js (App Router)** frontend. It provides core domains: Authentication, Content Management, Events & RSVPs, Notifications, AI Assistance, Site Configuration, and a pluggable Module System.

### Core Pillars
- **API First:** All functionality exposed via structured REST endpoints under `/api/*`.
- **Async Stack:** Async PostgreSQL access (SQLAlchemy + asyncpg) + async external HTTP (httpx) + async email workflows.
- **Extensibility:** Module and AI provider abstraction for future plug-ins.
- **Separation of Concerns:** Frontend consumes backend via a clean `api-client` wrapper.

```
Frontend (Next.js) -> api-client.ts -> FastAPI Routers -> Services / DB Models -> PostgreSQL & External Providers
```

## 2. Backend Components

| Component | File(s) | Purpose | Key Dependencies | Complexity |
|----------|---------|---------|------------------|------------|
| Application Entrypoint | `backend/main.py` | Creates FastAPI app, initializes DB, mounts routers, sets CORS | FastAPI, CORSMiddleware | Beginner–Intermediate |
| Configuration | `backend/config.py` | Centralized environment-driven settings (DB URL, secrets, SMTP, AI keys) | pydantic-settings, os | Beginner |
| Database & ORM | `backend/database.py` | Async engine + session + model declarations (User, Content, Module, etc.) | SQLAlchemy async, asyncpg | Intermediate |
| Auth Logic | `backend/auth.py`, `backend/routers/auth.py` | JWT issuance, password hashing, current user dependency, registration | passlib, jose, FastAPI security | Intermediate |
| AI Assistant | `backend/routers/ai_assistant.py`, `backend/models/ai_models.py` | Multi-provider AI abstraction (OpenRouter/OpenAI/Anthropic) | httpx, Pydantic, SQLAlchemy | Advanced |
| Content Management | `backend/routers/content.py` | CRUD + slug generation + AI suggestions placeholder | SQLAlchemy, regex | Intermediate |
| Module Management | `backend/routers/modules.py` | Install/configure/activate pluggable feature modules | SQLAlchemy | Intermediate |
| Site Settings | `backend/routers/settings.py` | Key/value config store & bulk site config merging | SQLAlchemy, Pydantic | Intermediate |
| Events & RSVPs | `backend/routers/events.py` | Event lifecycle, RSVP tracking, analytics | SQLAlchemy aggregates | Advanced |
| Notifications | `backend/routers/notifications.py` | Invitation/reminder sending, stats, templates registry | BackgroundTasks, SQLAlchemy | Advanced |
| Notification Service | `backend/services/notification_service.py` | SMTP email composition + logging + reminder logic | smtplib, email.mime | Advanced |
| Dashboard | `backend/routers/dashboard.py` | Aggregated metrics (content, modules, users) & analytics | SQLAlchemy aggregates | Intermediate |

### Models Summary
- **User**: Auth identity, preferences, roles.
- **Content**: Articles/pages with SEO + AI suggestion fields.
- **Module**: Installed feature definitions with JSON config & API keys.
- **AIProvider**: Active/fallback model provider records.
- **SiteSettings**: Key/value site configuration store.
- **Event**: Timed event with RSVP & reminder metadata.
- **RSVP**: Attendee responses + tracking fields.
- **Communication**: Email delivery log (invites, reminders, confirmations).

### Notable Backend Patterns
- Dependency injection for DB sessions (`get_db`) and current user (`get_current_user`).
- Async external calls (AI HTTP + SMTP (sync inside async boundary—could be offloaded)).
- Centralized config object reused across subsystems.

## 3. Frontend Components

| Category | Directory | Purpose | Backend Touchpoints | Complexity |
|----------|-----------|---------|---------------------|------------|
| Pages (App Router) | `app/*` | Route-level UI surfaces for each domain (content, modules, events, settings, auth) | All `/api/*` endpoints via client | Intermediate |
| Auth Forms | `components/auth/*` | Login & signup flows | `/api/auth/*` | Beginner–Intermediate |
| Content UI | `components/content/*` | Editor, listing, AI assistant integration | `/api/content`, `/api/ai` | Intermediate |
| Events UI | `components/events/*` | Event creation, listing, notification visibility | `/api/events`, `/api/notifications` | Intermediate–Advanced |
| Modules UI | `components/modules/*` | Catalog, install, configure, activation flows | `/api/modules/*` | Intermediate |
| Settings UI | `components/settings/*` | Site config + AI provider management | `/api/settings`, `/api/ai/providers` | Intermediate |
| Dashboard UI | `components/dashboard/*` | Overview metrics and quick actions | `/api/dashboard/*` | Beginner–Intermediate |
| Theme / Provider | `components/theme-provider.tsx`, `theme-toggle.tsx` | Dark/light theme support | None (client state) | Beginner |
| UI Primitives | `components/ui/*` | Design system wrappers (Radix + Tailwind) | Consumed internally | Beginner–Intermediate |
| API Client | `lib/api-client.ts` | Central HTTP wrapper with token handling | All routers | Intermediate |
| Utilities | `lib/utils.ts` | Style composition helper | N/A | Beginner |

### Frontend Flow
1. User interacts with a UI component (e.g., create content).
2. Component calls method on `apiClient`.
3. `apiClient` attaches JWT if present, performs fetch.
4. Response JSON returned to component for rendering/state updates.

## 4. API Surface (Representative)

| Domain | Base Path | Key Endpoints |
|--------|-----------|---------------|
| Auth | `/api/auth` | `POST /register`, `POST /token`, `GET /me` |
| Content | `/api/content` | `POST /`, `GET /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`, `POST /{id}/ai-suggestions` |
| AI | `/api/ai` | `POST /generate-content`, `GET /providers`, `POST /providers` |
| Modules | `/api/modules` | `GET /available`, `GET /installed`, `POST /install/{name}`, `PUT /{id}`, `POST /{id}/activate|deactivate`, `DELETE /{id}` |
| Settings | `/api/settings` | CRUD + `GET /config/site`, `POST /config/site`, `POST /initialize-defaults` |
| Events | `/api/events` | `GET /`, `POST /`, `GET /{id}`, `PUT /{id}`, `POST /{id}/rsvps`, `PUT /rsvps/{rsvp_id}`, `GET /{id}/analytics` |
| Notifications | `/api/notifications` | `POST /{event_id}/send-invitations`, `POST /{event_id}/send-reminders`, `GET /{event_id}/communications`, `GET /{event_id}/notification-stats`, `POST /test-email` |
| Dashboard | `/api/dashboard` | `GET /stats`, `GET /quick-actions`, `GET /analytics?days=` |

## 5. AI Provider Abstraction
- Providers stored in `AIProvider` table with `is_active` flag.
- Dynamic header templating per provider.
- Can expand by appending to `AIProviderManager.providers` mapping.
- Current response extraction assumes OpenAI-style `.choices[0].message.content` shape—adjust for Anthropic message variants.

## 6. Notification & Email System
- SMTP credentials driven by config.
- `NotificationService` builds HTML templates inline for invitations, reminders, confirmations.
- Communications logged for analytics (open/click placeholders—currently stored fields without tracking pixel implementation).
- Reminder scheduling logic present but would benefit from external scheduler / queue for robustness.

## 7. Module System
- Static catalog (`AVAILABLE_MODULES`) describes features and required config keys.
- Installation persists instance to `Module` table with JSON configuration + API key placeholders.
- Activation toggles `is_active` flag; no runtime plugin loading yet (foundation for future dynamic execution hooks).

## 8. Settings & Site Configuration
- Fine-grained key/value pairs in `SiteSettings` table.
- Bulk site config projection merges DB values over defaults (enables partial overrides).
- Initialization endpoint seeds defaults for cold start.

## 9. Security Model
| Aspect | Current | Suggested Enhancement |
|--------|---------|-----------------------|
| Auth Tokens | Short-lived access tokens (30m) | Add refresh token rotation + revoke table |
| Passwords | Bcrypt hashing | Enforce complexity & rate limit login |
| Secrets | Plain environment variables | Use secret manager or vault, rotate periodically |
| API Keys (Modules/AI) | Stored raw in DB JSON | Encrypt at rest (Fernet or KMS) |
| Rate Limiting | None | Apply per-IP & per-endpoint throttles |
| Audit Logging | Minimal | Add structured logs with correlation IDs |

## 10. Scalability & Performance Considerations
| Area | Current State | Scaling Path |
|------|---------------|-------------|
| DB Load | Simple CRUD + aggregates | Add indexes, caching layer (Redis) for hot counts |
| AI Calls | Direct HTTP each request | Add retry/backoff & caching for idempotent prompts |
| Email Sending | Inline in background tasks | Move to queue (Celery/RQ) + worker autoscale |
| Analytics Queries | On-demand aggregates | Precompute or materialized views for heavy dashboards |
| Static Assets | Basic public folder | CDN front + image optimization pipeline |

## 11. Suggested Next Steps (Roadmap)
1. Introduce Alembic migrations for schema evolution.
2. Add SQLAlchemy relationships for clearer ORM navigation.
3. Implement centralized logging + error handler middleware.
4. Encrypt sensitive API keys at write/read boundaries.
5. Externalize email templates (Jinja2) for maintainability.
6. Adopt SWR / React Query on frontend for caching and revalidation.
7. Add unit/integration tests (Auth, Content slug, RSVP lifecycle, AI fallback path).
8. Add rate limiting & request metrics.
9. Implement refresh token or session rotation.
10. Add feature flags for experimental modules.

## 12. Glossary
| Term | Definition |
|------|------------|
| Module | A pluggable feature entity persisted in DB with config & activation state |
| AI Provider | External LLM service configuration record (OpenRouter/OpenAI/Anthropic) |
| Communication | Logged outbound email metadata for analytics |
| Site Config | Merged dataset of defaults + stored overrides served to frontend |

## 13. Maintenance Tips
- Keep `config.py` minimal—prefer hierarchical settings if growth continues.
- Introduce DTO boundaries if frontend/backend contracts expand.
- Monitor slow query logs; add indexes proactively (e.g., `Content.slug`, `Event.start_date`, `RSVP.event_id`).
- Consider a health detail endpoint that verifies DB + SMTP + AI provider readiness.

## 14. License & Attribution (Placeholder)
Add license information if open-sourcing; include provider usage notices if required (e.g., OpenRouter attribution headers already present).

---
Generated automatically – update as architecture evolves.

---

## 15. Extended Component Exploration (Chronological & Layered)

Below augments prior sections with a unified, deeper catalog. Existing descriptions retained; duplicates only consolidated where identical.

### 15.1 Chronological Build-Up
1. Configuration & Settings load (`config.py`) → environment drives secrets & endpoints.
2. Database initialization (`database.py:init_db`) prepares tables (no migrations yet).
3. FastAPI app assembly (`main.py`) mounts routers & CORS.
4. Authentication flow (`auth` router) enables session tokens.
5. Core domain CRUD (Content, Modules, Settings) establishes baseline CMS functionality.
6. Event & RSVP domain adds temporal engagement layer.
7. Notification service + router introduces outbound email & communication logs.
8. AI Assistant router layers intelligent content augmentation.
9. Dashboard router aggregates cross-domain analytics.
10. Frontend pages & components consume all above via `api-client`.

### 15.2 Consolidated Components Table

| Component | Layer | Description | Key Dependencies | Interactions | Complexity |
|-----------|-------|-------------|------------------|--------------|------------|
| Settings Config | Infra | Central environment settings | pydantic-settings | Used by auth, DB, AI, SMTP | Beginner |
| Database Init & Models | Infra | Engine/session + ORM tables | SQLAlchemy async | All routers/services | Intermediate |
| App Entrypoint | Infra | FastAPI app + router mounting | FastAPI | All HTTP traffic | Beginner–Intermediate |
| Auth Router | API | JWT issuance & identity | passlib, jose | Protects other routers | Intermediate |
| Content Router | API | Content CRUD + slug logic | SQLAlchemy | Dashboard, future AI synergy | Intermediate |
| Modules Router | API | Module lifecycle mgmt | SQLAlchemy | Dashboard stats | Beginner–Intermediate |
| Settings Router | API | Site K/V & bulk config | SQLAlchemy, Pydantic | Frontend branding/config | Intermediate |
| Events Router | API | Event + RSVP + analytics | SQLAlchemy aggregates | Notifications, Dashboard | Advanced |
| Notifications Router | API | Emails (invites/reminders) & logs | BackgroundTasks, SMTP | Events, Communication | Advanced |
| AI Assistant Router | API | Multi-provider AI abstraction | httpx, AIProvider | Content editor, AI UI | Advanced |
| Dashboard Router | API | Aggregated metrics & timelines | SQLAlchemy | Frontend overview | Beginner–Intermediate |
| NotificationService | Service | SMTP sending + logging | smtplib, email.mime | Notifications router | Advanced |
| AI Provider Manager | Service | Provider selection & request dispatch | httpx | AI Assistant | Advanced |
| Slug Generator | Utility | Title → slug transformation | regex | Content create/update | Beginner |
| API Client | Frontend Utility | Fetch with auth header injection | fetch/localStorage | All backend APIs | Beginner |
| UI Primitives | Frontend Library | Button/input/dialog core components | Tailwind, Radix | Other UI components | Beginner–Intermediate |
| Content Editor UI | Frontend Feature | Authoring & AI assist surface | React, API client | Content + AI APIs | Intermediate |
| Events UI | Frontend Feature | Manage events & view RSVPs | React | Events + Notifications APIs | Intermediate–Advanced |
| Modules UI | Frontend Feature | Install & configure modules | React | Modules API | Intermediate |
| Settings UI | Frontend Feature | Modify site/provider/user config | React | Settings + AI provider APIs | Intermediate |
| Dashboard UI | Frontend Feature | Present system analytics | React | Dashboard API | Beginner–Intermediate |
| Theme Provider | Frontend Infra | Theme context & dark mode | next-themes | Wraps all UI | Beginner |

### 15.3 Dependency & Interaction Mapping

```
Browser UI -> api-client -> FastAPI Routers -> (DB Models | Services) -> DB / External (SMTP, AI APIs)
													^
										  Config (env settings)
```

Interaction Highlights:
- Auth token dependency cascades into every protected router method.
- Events ↔ Notifications: invitations & reminders generate `Communication` rows.
- AI Assistant optionally complements Content authoring (future real integration beyond mock suggestions route).
- Dashboard aggregates counts across Content, Modules, Users, Events.

### 15.4 Complexity Rationale Summary

| Complexity Tier | Examples | Rationale |
|-----------------|----------|-----------|
| Beginner | Slug generator, Theme toggle | Pure functions or minimal state/logic |
| Intermediate | Content router, Settings router, Modules UI | CRUD + light validation/state transitions |
| Advanced | AI Assistant, Notifications, Events analytics | External I/O, aggregation, mixed access patterns, potential error resilience needs |

### 15.5 Opportunities & Evolution (Merged Overview)

| Area | Immediate Enhancement | Strategic Direction |
|------|-----------------------|---------------------|
| Auth | Add refresh tokens & role dependency | Full RBAC + SSO/OAuth federation |
| AI | Timeouts + usage metrics | Streaming & tool augmentation |
| Notifications | Queue + template externalization | Event-driven pipeline & analytics dashboard |
| Modules | Persist dynamic catalog | Plugin sandbox/runtime isolation |
| Content | DB indexes + full-text search | Versioning & editorial workflow |
| Observability | Request/DB metrics + structured logs | Distributed tracing & anomaly detection |
| Security | Rate limiting & secret masking | Centralized secret manager, key rotation |

### 15.6 Cross-Cutting Quality Checklist

- [ ] Add Alembic migrations.
- [ ] Standardize response models (avoid raw ORM leakage).
- [ ] Introduce request ID middleware & structured logging.
- [ ] Encrypt stored API keys (Fernet/KMS envelope).
- [ ] Implement refresh token rotation & revocation list.
- [ ] Add role-based `requires_roles()` dependency.
- [ ] Rate limit auth + AI endpoints.
- [ ] Replace duplicate invitation logic in events vs notifications routers.
- [ ] Externalize email templates (Jinja2) and add localization hooks.
- [ ] Add indexing: `content.slug`, `event.start_date`, `rsvp.event_id`.

### 15.7 Glossary Additions

| Term | Definition |
|------|------------|
| RSVP Public Access | Public-facing endpoints enabling unauthenticated RSVP creation/update (currently by numeric ID) |
| Communication Log | Persistence layer capturing email send metadata for analytics & auditing |
| Provider Manager | AI routing layer selecting active provider & shaping requests |

---
End of extended component exploration (appended).
