# Portfolio API Reference

This guide catalogues every endpoint used by the standalone portfolio frontend (`Frontend/`) and how it maps back to the CMS backend. Use it as a directory when you need to swap data sources, add new sections, or point staging builds at a different environment.

## Base URLs & Environment Variables

| Context                | Variable                | Default             | Notes |
|------------------------|-------------------------|---------------------|-------|
| Backend FastAPI server | `DATABASE_URL`, `SECRET_KEY`, etc. | See `backend/config.py` | Managed server side. |
| Frontend API base URL  | `VITE_API_URL` (Vite) or `REACT_APP_API_URL` (CRA) | `http://localhost:8000` | Set via `.env.local` to target staging/production. |
| Extra CORS origins     | `ALLOWED_ORIGINS`       | _optional_          | Comma separated origins appended to defaults. |

> The frontend `portfolioAPI` helper reads `VITE_API_URL` first. Fallback to `REACT_APP_API_URL` keeps compatibility with Create React App.

## Public Portfolio Endpoints

All endpoints below are unauthenticated. Each one also ships under `/api/v1/portfolio/*` for backwards compatibility but new code should prefer the `/api/public` namespace.

| Purpose                  | Method & Path                         | Query Parameters                       | Response Model |
|--------------------------|---------------------------------------|----------------------------------------|----------------|
| Portfolio summary        | `GET /api/public/profile`             | –                                      | `PortfolioSummarySchema` |
| Hero metrics             | `GET /api/public/stats`               | –                                      | `PortfolioStatSchema[]` |
| Skills catalogue         | `GET /api/public/skills`              | `featured_only`, `category`            | `SkillSchema[]` |
| Projects list            | `GET /api/public/projects`            | `featured_only`, `category`, `limit`   | `ProjectSchema[]` |
| Project detail           | `GET /api/public/projects/{id}`       | –                                      | `ProjectSchema` |
| Project categories       | `GET /api/public/project-categories`  | –                                      | `ProjectCategorySchema[]` |
| Experience timeline      | `GET /api/public/experience`          | `featured_only`                        | `ExperienceSchema[]` |
| Testimonials             | `GET /api/public/testimonials`        | `featured_only`, `limit`               | `TestimonialSchema[]` |
| Homepage bundle          | `GET /api/public/homepage-data`       | –                                      | `HomepageDataSchema` |
| Full portfolio snapshot  | `GET /api/public/portfolio-overview`  | –                                      | `PortfolioOverviewSchema` |

The FastAPI models live in `backend/routers/portfolio.py`. Default data comes from `backend/services/portfolio_data.py` which centralises the fixtures until database tables are introduced.

## AI Assistant Endpoints

| Purpose                 | Method & Path              | Auth | Notes |
|-------------------------|----------------------------|------|-------|
| List providers          | `GET /api/ai/providers`    | ✅    | Admin UI to audit configured models. |
| Upsert provider         | `POST /api/ai/providers`   | ✅    | Requires `admin` role; encrypts API keys. |
| Authenticated generation| `POST /api/ai/generate-content` | ✅ | Used by the CMS editor. |
| Portfolio chatbot       | `POST /api/ai/public/chat` | ❌    | Public endpoint for the marketing site. |

The `AIProviderManager` handles provider-specific payloads, injecting decrypted keys and respecting per-provider defaults. Adding a new provider only requires extending `AIProviderManager.providers` with a `base_url`, `default_model`, and `headers_template`.

### Request Payload

The `POST /api/ai/public/chat` endpoint expects the shared `AIRequest` schema:

```jsonc
{
  "prompt": "What experience does Ryan have with Power BI?",
  "model": "optional-model-name",
  "temperature": 0.7,
  "max_tokens": 800,
  "context": "Optional system instructions"
}
```

Responses always conform to `AIResponse`:

```json
{
  "content": "I have 8+ years delivering Power BI dashboards...",
  "provider": "openrouter",
  "model": "meta-llama/llama-3.1-8b-instruct:free",
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 64
  }
}
```

## Frontend Consumption Map

| Frontend Hook / Component        | Backend Endpoint(s)                     | File |
|----------------------------------|------------------------------------------|------|
| `useHomepageData`                | `GET /api/public/homepage-data`          | `Frontend/hooks/usePortfolio.js` |
| `SkillsGrid`                     | `GET /api/public/skills`                 | `Frontend/components/SkillsGrid.jsx` |
| `ProjectsGrid`                   | `GET /api/public/projects`               | `Frontend/components/ProjectsGrid.jsx` |
| `useProjects`                    | `GET /api/public/projects`               | `Frontend/hooks/usePortfolio.js` |
| `useProject`                     | `GET /api/public/projects/{id}`          | `Frontend/hooks/usePortfolio.js` |
| `useExperience`                  | `GET /api/public/experience`             | `Frontend/hooks/usePortfolio.js` |
| `useTestimonials`                | `GET /api/public/testimonials`           | `Frontend/hooks/usePortfolio.js` |
| ChatBot                          | `POST /api/ai/public/chat` (fallback to local heuristics) | `Frontend/ChatBot.jsx` |

## Swapping Data Sources

1. **Add database models** in `backend/models/portfolio_models.py` (placeholder import already wired in the service layer).
2. **Update `PortfolioDataService`** methods to query SQLAlchemy models before falling back to fixtures.
3. **Extend the frontend service** (`Frontend/services/portfolioAPI.js`) if you introduce new endpoints.
4. **Document the changes** by appending to this file so future swaps remain frictionless.

## Testing Checklist

- `npm run dev` (in `Frontend/`) should load the portfolio with live data.
- `uvicorn backend.main:app --reload` exposes the API endpoints.
- `curl http://localhost:8000/api/public/homepage-data` verifies the aggregate payload.
- Configure an AI provider via `POST /api/ai/providers` then hit `POST /api/ai/public/chat` to confirm the chatbot path.

Keep this reference close when adjusting integrations—the goal is to make backend/ frontend swaps predictable and well documented.
