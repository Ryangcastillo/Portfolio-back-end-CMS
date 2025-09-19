# Stitch CMS – Backend API & Services Catalog

> Generated catalog of current FastAPI backend (routers, endpoints, models, side-effects) plus security / scalability recommendations.

## 1. High-Level Architecture

- Entry point: `backend/main.py` wires routers under `/api/*` prefixes.
- Persistence: Async SQLAlchemy models in `backend/database.py` (no explicit relationship() helpers yet; implicit foreign keys only).
- Auth: Username/password → JWT bearer (`/api/auth/token`), 15–`access_token_expire_minutes` minute expiry (configurable). No refresh token layer.
- Domains (Routers):
  - Authentication: `/api/auth` – registration, token issuance, identity.
  - Content Management: `/api/content` – CRUD + AI suggestion placeholder.
  - Modules: `/api/modules` – install/activate/update catalogued “pluggable” features.
  - Settings: `/api/settings` – K/V site configuration & bulk site config operations.
  - AI Assistant: `/api/ai` – multi‑provider abstraction for LLM content generation.
  - Events: `/api/events` – event lifecycle, RSVPs, analytics (mixed public + protected endpoints).
  - Notifications: `/api/notifications` – email invitation/reminder orchestration (background tasks).
  - Dashboard: `/api/dashboard` – aggregate metrics & analytics timelines.

## 2. Authentication / User Management Deep Dive

| Concern | Current Implementation | Gaps / Risks | Recommended Improvement |
|---------|------------------------|--------------|-------------------------|
| Password hashing | `passlib` bcrypt | OK | Add pepper (env) + rehash check on login. |
| JWT creation | HS256 single secret | No key rotation, no audience/issuer, 401 only | Include `aud`, `iss`; implement key rotation (kid header) & short access + refresh pair. |
| Token scope / roles | `role` field exists on `User` model but unused in dependencies | No route-level RBAC; all authenticated users equal | Introduce `@requires_roles([...])` dependency, or claim-based authorization. |
| Session invalidation | None (stateless) | Cannot revoke compromised tokens | Add token blacklist (short TTL) or rotate refresh tokens (token family). |
| Registration | Open endpoint `/register` | No email verification / rate limiting | Add verification token + throttling (by IP/email). |
| Password reset | Not implemented | Usability gap | Implement reset token flow (signed, short-lived). |
| Brute force defense | None | Credential stuffing risk | Track failed attempts → exponential backoff or temporary lock. |
| Logging & audit | Not present | Hard to trace auth issues | Add structured logging (user_id, ip, action) and optional audit table. |

JWT Payload Today: `{ "sub": username, "exp": <utc ts> }`

Suggested Extended Payload: `{ "sub": user_id, "uname": username, "role": role, "iat": ts, "exp": ts, "aud": "stitch-cms", "iss": "stitch-cms-api" }`.

Refresh Strategy (proposed):
1. Short-lived access token (15m) + refresh token (7–30d) stored HTTP-only secure cookie.
2. `/api/auth/refresh` issues new pair; old refresh token invalidated (rotating). Maintain table: id, user_id, family_id, expires_at, revoked_at.
3. Logout revokes active refresh token(s).

## 3. Router Overview Summary

| Router | Prefix | Tag | Primary Entities | Auth Required? | Public Endpoints | Notes |
|--------|--------|-----|------------------|----------------|------------------|-------|
| auth | /api/auth | Authentication | User | Mixed | `/register`, `/token` | Lacks email verification & refresh flows. |
| content | /api/content | Content Management | Content | Yes | None | AI suggestions mocked. |
| modules | /api/modules | Module Management | Module | Yes | None | Uses in-memory AVAILABLE_MODULES catalog. |
| settings | /api/settings | Settings | SiteSettings | Yes | None | Bulk site config & defaults init. |
| ai_assistant | /api/ai | AI Assistant | AIProvider | Yes | None | External API proxying (OpenRouter/OpenAI/Anthropic). |
| events | /api/events | Event Management | Event, RSVP | Mixed | `POST /{id}/rsvps`, `PUT /rsvps/{rsvp_id}` | Invitation sending duplicated in notifications router. |
| notifications | /api/notifications | Notifications | Communication, Event, RSVP | Yes | None | Uses background tasks for email send/reminders. |
| dashboard | /api/dashboard | Dashboard | Aggregates | Yes | None | Lightweight analytics (SQL counts). |

## 4. Detailed Endpoint Catalog

Legend: Auth = Bearer token required; Side Effects = DB writes, external calls, background tasks; Models listed are request bodies unless otherwise stated.

### 4.1 Authentication (`/api/auth`)

| Method | Path | Auth | Request Model | Response | Side Effects | Notes |
|--------|------|------|---------------|----------|--------------|-------|
| POST | /register | No | UserCreate | UserResponse | Insert User | No uniqueness check on username (only email). |
| POST | /token | No | OAuth2PasswordRequestForm | Token | None | Username used as `sub`; rate limiting absent. |
| GET | /me | Yes | – | UserResponse | None | Returns DB user directly. |

Improvements: Add `/refresh`, `/logout`, `/verify-email`, `/password-reset`.

### 4.2 Content (`/api/content`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| POST | / | Yes | ContentCreate | ContentResponse | Insert Content | Slug uniqueness loop (O(n) queries). Use single COUNT or add unique index & retry. |
| GET | / | Yes | Query params | List[ContentResponse] | None | Search uses `ilike` across 3 columns (no indexes). |
| GET | /{id} | Yes | – | ContentResponse | None | 404 if absent. |
| PUT | /{id} | Yes | ContentUpdate | ContentResponse | Update Content | Updates slug; race not locked. |
| DELETE | /{id} | Yes | – | {message} | Delete row | Hard delete. |
| POST | /{id}/ai-suggestions | Yes | – | suggestions(json) | Update `ai_suggestions` JSON | Currently mock; no provider call. |

### 4.3 Modules (`/api/modules`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| GET | /available | Yes | category? | List[AvailableModule] | None | In-memory static list (non-db). |
| GET | /installed | Yes | – | List[ModuleResponse] | None | Returns all modules. |
| POST | /install/{name} | Yes | ModuleCreate | {message, module_id} | Insert Module | Forces inactive start. |
| PUT | /{id} | Yes | ModuleUpdate | {message} | Update Module | Bulk setattr; no field validation beyond pydantic types. |
| POST | /{id}/activate | Yes | – | {message} | Set is_active True | No dependency checks. |
| POST | /{id}/deactivate | Yes | – | {message} | Set is_active False | – |
| DELETE | /{id} | Yes | – | {message} | Delete Module | No cascade clean-up. |

### 4.4 Settings (`/api/settings`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| GET | / | Yes | – | List[SettingResponse] | None | Returns raw values (no masking). |
| GET | /{key} | Yes | – | SettingResponse | None | 404 if missing. |
| POST | / | Yes | SettingCreate | SettingResponse | Insert setting | 400 if exists. |
| PUT | /{key} | Yes | SettingUpdate | SettingResponse | Update setting | Value type arbitrary (Any). |
| DELETE | /{key} | Yes | – | {message} | Delete row | – |
| GET | /config/site | Yes | – | SiteConfig | None | Merges defaults + overrides. |
| POST | /config/site | Yes | SiteConfig | {message} | Upsert multiple | No per-field audit. |
| POST | /initialize-defaults | Yes | – | {message} | Seed defaults | Idempotent-ish (skips existing). |

### 4.5 AI Assistant (`/api/ai`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| POST | /generate-content | Yes | AIRequest | AIResponse | External HTTP call | Provider selection: first active; errors proxied. |
| GET | /providers | Yes | – | List[provider summary] | None | Exposes `has_api_key` only (good). |
| POST | /providers | Yes | AIProviderConfig | {message, provider_id} | Insert/Update provider(s) | Deactivates others if active, but logic re-queries twice. |

Hardening Suggestions: Timeout, retry/backoff, rate limiting per user, streaming support, model allowlist.

### 4.6 Events (`/api/events`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| GET | / | Yes | Query params | List[EventResponse] | Aggregation queries | Aggregates RSVP counts per event. |
| POST | / | Yes | EventCreate | {message, event_id} | Insert Event | Sets reminder config. |
| GET | /{id} | Yes | – | {event, rsvps[]} | None | Returns raw ORM objects (not pydantic). |
| PUT | /{id} | Yes | EventUpdate | {message} | Update Event | No validation of date ordering. |
| POST | /{id}/rsvps | No | RSVPCreate | {message, rsvp_id} | Insert RSVP | Public; invites email uniqueness enforced. |
| PUT | /rsvps/{rsvp_id} | No | RSVPUpdate | {message} | Update RSVP | Anyone w/ rsvp_id can update (no token). |
| POST | /{id}/send-invitations | Yes | List[str] | {message} | Insert RSVPs | Duplicate of notifications router’s invitations (overlap). |
| GET | /{id}/analytics | Yes | – | summary + timeline | Aggregations | Response rate computed (accepted/total_invites). |

Public RSVP security: Consider signed token in invitation link instead of open numeric id.

### 4.7 Notifications (`/api/notifications`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| POST | /{event_id}/send-invitations | Yes | SendInvitationsRequest | {message} | Create RSVPs + enqueue background email tasks | Overlaps with events endpoint.
| POST | /{event_id}/send-reminders | Yes | – | {message} | Background reminder tasks | Calculates days_until at runtime.
| GET | /{event_id}/communications | Yes | pagination | List[Communication] | None | Returns raw Communication (no schema). |
| GET | /{event_id}/notification-stats | Yes | – | NotificationStats | Aggregations | Uses SQL CASE for metrics. |
| GET | /templates | Yes | – | List[templates] | None | Static list. |

### 4.8 Dashboard (`/api/dashboard`)

| Method | Path | Auth | Request | Response | Side Effects | Notes |
|--------|------|------|---------|----------|--------------|-------|
| GET | /stats | Yes | – | DashboardStats | Multiple count queries | Could batch w/ CTE or fewer round-trips. |
| GET | /quick-actions | Yes | – | List[QuickAction] | None | Static curated actions. |
| GET | /analytics | Yes | days? | summary + timelines | Aggregations | Timeline by created_at date. |

## 5. Cross-Cutting Observations

| Category | Current State | Improvement Ideas |
|----------|---------------|------------------|
| Validation | Pydantic request models but responses sometimes raw ORM (events, notifications communications) | Add `response_model` consistently + `orm_mode` for safety & filtering. |
| Consistency | Some endpoints return `{message: ...}`, others full objects | Adopt uniform envelope (e.g., `{data, meta}`) or pure resource style per REST. |
| Error Semantics | Mostly 400/401/404; lacks 422 differentiation for business rules | Use domain-specific error codes + structured error model. |
| Pagination | Only `skip/limit` on some lists | Standardize `page/page_size` or cursor-based where large growth expected. |
| N+1 / Queries | Separate count queries; loops (slug generation) | Use DB constraints + exception handling, aggregate queries w/ grouping. |
| Indexing | Filters on `Content.slug`, `Content.status`, `Content.content_type`, etc. | Add indexes to reduce full scans. |
| Security | Public RSVP update by id, no rate limiting | Introduce signed token or per-email verification + global throttling. |
| Secrets Exposure | Settings returns raw values (some may be secrets) | Mark sensitive keys & mask values on GET. |
| Observability | No logging/tracing/metrics | Add structured logs + OpenTelemetry instrumentation + request IDs. |
| Background Work | FastAPI BackgroundTasks only | Migrate heavier tasks to queue (Celery / RQ / Dramatiq) for retries + scheduling. |
| AI Requests | Direct pass-through, no timeout config surfaced | Add timeouts, circuit breaker, model allow/deny lists, usage quotas. |
| Data Lifecycle | Hard deletes (content/modules) | Consider soft deletes (deleted_at) for recovery & audit. |

## 6. Recommended Roadmap (Backend-Focused)

Short Term (1–2 sprints):
1. Add response models to every endpoint returning ORM objects (events detail, communications list).
2. Implement role claim in JWT and RBAC dependency for admin-only routes (e.g., module install, settings changes).
3. Add unique DB constraints & indexes (users.email, users.username, content.slug, module.name) + handle IntegrityError.
4. Secure public RSVP flow via signed token in invitation links; restrict update to possession of token.
5. Extract duplicated invitation logic from `events` router into notifications service only (remove duplication).

Mid Term (3–5 sprints):
6. Introduce refresh token flow + email verification.
7. Add centralized error handler producing structured errors.
8. Implement rate limiting (e.g., Redis sliding window) on auth + AI endpoints.
9. Add task queue (Celery/Dramatiq) for email + reminder scheduling with retries.
10. Observability: logging, metrics (Prometheus), tracing (OTel). 

Long Term:
11. Modular plugin system persisted in DB (replace static AVAILABLE_MODULES) with migration support & dynamic discovery.
12. Versioned content & draft publishing workflows.
13. Full-text search (PostgreSQL tsvector) for content search scalability.
14. Multi-tenancy (org_id / site_id column) if SaaS direction.
15. Secrets management integration (AWS Secrets Manager / Vault) for provider API keys.

## 7. Data Model Coverage vs API

| Model | Exposed CRUD? | Notes |
|-------|---------------|-------|
| User | Partial (register, me) | Lacks admin user management endpoints. |
| Content | Full CRUD | AI fields present but partially leveraged. |
| Module | Full CRUD (install/update/delete + activation) | Install path is custom; no listing of AVAILABLE from DB. |
| SiteSettings | Full CRUD + bulk config | No masking/secrets classification. |
| AIProvider | Create/List + generate | No delete/deactivate endpoint (only active flag logic). |
| Event | Full CRUD (list, get, create, update) | No delete endpoint; maybe intentional. |
| RSVP | Create/Update (public) | No authenticated list per user; data returned bundled with event. |
| Communication | Read (list for event) | No creation endpoint (service handles inserts). |

## 8. Security Quick Wins Checklist

- [ ] Add `user.username` unique constraint & index.
- [ ] Add rate limit (e.g., 5 requests / 30s) on `/api/auth/token`.
- [ ] Add `aud`, `iss` to JWTs; rotate secret quarterly.
- [ ] Mask sensitive settings when key matches patterns: `key.endswith('_key') or 'secret' in key.lower()`.
- [ ] Validate date logic for events (`end_date >= start_date`, RSVP deadlines before start).
- [ ] Add request body size limit for AI prompts & content.
- [ ] Enforce allowed `content_type` enumeration (article, page, etc.).
- [ ] Add CORS dynamic origin allowlist via config.

## 9. Example Enhanced Dependency (RBAC Skeleton)

```python
from fastapi import Depends, HTTPException, status

def requires_roles(*roles):
    def wrapper(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user
    return wrapper

# Usage:
# @router.post("/install/{module_name}")
# async def install_module(..., current_user=Depends(requires_roles("admin"))):
```

## 10. Testing & Quality Recommendations

| Test Type | Priority | Focus |
|-----------|----------|-------|
| Unit | High | Slug generation uniqueness; JWT creation/expiry validation. |
| Integration | High | Registration → login → protected route access; module install/activate lifecycle. |
| Security | Medium | Brute force mitigation; public RSVP endpoint abuse. |
| Load | Medium | `/api/content` list under large dataset; AI provider latency timeouts. |
| Regression | Medium | Settings bulk update idempotency; event analytics accuracy. |

Suggested Tools: `pytest-asyncio`, `httpx.AsyncClient` test client, `pytest-cov`, `factory_boy` for fixtures.

## 11. Observability Blueprint

| Layer | Metric / Log | Purpose |
|-------|--------------|---------|
| Auth | login_success, login_failure (counter) | Security monitoring |
| Content | content_created, content_published (counter) | Growth tracking |
| AI | ai_request_latency (histogram), ai_request_failures (counter) | Provider health |
| Notifications | emails_sent, emails_failed (counter) | Deliverability insight |
| DB | connection_pool_in_use, query_duration | Performance baselines |

Add correlation IDs: middleware injecting `X-Request-ID` (uuid4) → include in logs & responses.

## 12. Conclusion

Current API surface is clear and modular, enabling rapid iteration. Priority improvements center on security hardening (JWT + public endpoints), consistency (response models), and production robustness (observability, background processing, indexing). The roadmap above sequences low-effort/high-impact enhancements first.

---
Generated automatically. Keep this file updated as endpoints evolve (consider automated extraction in CI using `fastapi.routing.APIRoute` introspection).
