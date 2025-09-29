# Frontend Integration Guide

This guide summarizes the API contracts that power the Stitch CMS frontend experiences so you can wire a landing page or dashboard quickly.

## Base URLs

- **Backend**: `http://localhost:8000`
- **Production Example**: `https://<your-vercel-app>.vercel.app`

All secure endpoints require a `Bearer` token generated from the authentication endpoints:
- `/api/auth/token` - For regular users (editor, viewer roles)  
- `/api/auth/neon-auth` - For admin access via Neon authentication

**Note**: Admin users cannot login via `/api/auth/token` - they must use Neon authentication.

## Public Landing Page Data

| Section            | Endpoint                                   | Notes |
|-------------------|--------------------------------------------|-------|
| Hero / About       | `GET /api/v1/portfolio/summary`            | Returns name, title, bio, contact links, resume URL. |
| Featured Projects  | `GET /api/v1/portfolio/projects?featured_only=true` | Use the `featured_only` query to control hero cards. |
| Skills Grid        | `GET /api/v1/portfolio/skills`             | Already grouped by category; great for tabbed layouts. |
| Timeline           | `GET /api/v1/portfolio/experience`         | Contains chronological work history with `is_current` flag. |
| Testimonials (future) | Extend `/api/v1/portfolio` router once testimonial model is added. |

## Authenticated Dashboard Data

| Area          | Endpoint | Description |
|---------------|----------|-------------|
| Global Stats  | `GET /api/dashboard/stats` | Totals for content, users, modules, and recent activity feed. |
| Quick Actions | `GET /api/dashboard/quick-actions` | Preconfigured CTA cards for the admin UI. |
| Analytics     | `GET /api/dashboard/analytics?days=30` | Timeline of content creation and type breakdown. |

## Content Editing Workflows

1. **Create Draft** – `POST /api/content`
2. **Iterate** – `PUT /api/content/{id}`
3. **AI Suggestions** – `POST /api/content/{id}/ai-suggestions`
4. **Publish** – update `status` to `published` to auto-stamp `published_at`
5. **List & Filter** – `GET /api/content?status=published&content_type=page`

Use these to build an editorial UI or surface curated content on the marketing site.

## Settings for Landing Page Copy

- Structured key-value pairs: `GET/POST /api/settings`
- Bulk config: `GET/POST /api/settings/config/site`
- Initialize defaults: `POST /api/settings/initialize-defaults`

Recommended pattern: load `config/site` for layout scaffolding and query individual keys (e.g. `hero_headline`) for dynamic sections.

## Module Integrations

When enabling analytics or marketing add-ons from the dashboard:

1. `GET /api/modules/available`
2. `POST /api/modules/install/{module_name}` with configuration
3. `POST /api/modules/{id}/activate`

Encrypted API keys are handled automatically via `encrypt_value`; you only store plaintext on the client when collecting user input.

## AI Provider Setup

Configure once via:

- `POST /api/ai/providers`
- `POST /api/ai/generate-content`

Store the selected provider metadata client-side to toggle AI helpers in the UI.

## Integration Recommendations

- **Cache public endpoints** (portfolio data) with ISR/SWR on the Next.js landing page to reduce backend load.
- **Use optimistic updates** for content editing to keep the dashboard responsive.
- **Leverage module metadata** to render install/activate buttons without extra hardcoding.
- **Guard admin routes** by verifying tokens via `/api/auth/me` on page load.

See the accompanying [Postman collection](./postman/stitch-cms.postman_collection.json) for ready-to-import requests.
