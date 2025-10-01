# Frontend Integration Guide

This guide summarizes the API contracts that power the Stitch CMS frontend experiences so you can wire a landing page or dashboard quickly.

## Base URLs

- **Backend**: `http://localhost:8000`
- **Production Example**: `https://<your-vercel-app>.vercel.app`

All secure endpoints require a `Bearer` token generated from the `/api/auth/token` login flow.

## Public Landing Page Data

All marketing experiences can be powered via unauthenticated endpoints mounted under `/api/public`. The same handlers are also exposed under `/api/v1/portfolio/*` for backwards compatibility.

| Section            | Endpoint                                   | Notes |
|-------------------|--------------------------------------------|-------|
| Hero / About      | `GET /api/public/profile`                  | Returns name, title, biography, location, resume URL, and social links. |
| Stats strip       | `GET /api/public/stats`                    | Metric name/value pairs surfaced under the hero CTA. |
| Skills Grid       | `GET /api/public/skills`                   | Supports `featured_only=true` and `category=` filters. |
| Featured Projects | `GET /api/public/projects?featured_only=true&limit=3` | Use `category` and `limit` to slice cards per portfolio page. |
| Project Details   | `GET /api/public/projects/{id}`            | Returns the long description, impact metrics, and external links. |
| Categories        | `GET /api/public/project-categories`       | Aggregated counts for filters or tab navigation. |
| Timeline          | `GET /api/public/experience`               | Chronological work history with `achievements` highlights. |
| Testimonials      | `GET /api/public/testimonials`             | Optional `featured_only` and `limit` parameters for carousel sizing. |
| Homepage bundle   | `GET /api/public/homepage-data`            | Convenience payload combining profile, stats, featured skills, and featured projects. |
| Full overview     | `GET /api/public/portfolio-overview`       | One-shot payload that powers “About” or press kits. |

> **Environment variables**: The Vite bundle reads `VITE_API_URL`. Create a `.env.local` file with `VITE_API_URL=http://localhost:8000` (or export `REACT_APP_API_URL` when using Create React App).

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
- `POST /api/ai/public/chat`

The public chat endpoint powers the portfolio chatbot and honours the active provider + encrypted API key. Keep the key server-side—only the backend touches it.

## Integration Recommendations

- **Cache public endpoints** (portfolio data) with ISR/SWR on the Next.js landing page to reduce backend load.
- **Use optimistic updates** for content editing to keep the dashboard responsive.
- **Leverage module metadata** to render install/activate buttons without extra hardcoding.
- **Guard admin routes** by verifying tokens via `/api/auth/me` on page load.

See the accompanying [Postman collection](./postman/stitch-cms.postman_collection.json) for ready-to-import requests.
