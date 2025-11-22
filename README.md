## Mini Compliance Monitor

Mini Compliance Monitor is a full-stack compliance observability platform. The FastAPI backend stores events, runs rules, and enriches findings with AI, while the React + TypeScript dashboard visualizes stats, events, and findings in real time so you can monitor guards, drive investigations, and demonstrate the full data chain.

## Tech Stack

### Backend

- FastAPI for REST APIs and dependency injection
- SQLAlchemy for ORM models and session management
- Pydantic / `pydantic-settings` for schema validation and configuration
- OpenAI (via the `openai` client) to generate risk scores and explanations, with heuristics as a fallback

### Frontend

- React 18 with TypeScript, Vite 5, and shadcn/ui components
- Tailwind CSS for styling plus utility helpers from `clsx`, `class-variance-authority`, and `tailwind-merge`
- Recharts for severity bar charts and event timelines
- TanStack Query and React Router (already wired via the dependency graph) for scalable navigation and data fetching
- Central API client pattern in `frontend/src/api/` that wraps fetch calls and surfaces typed errors

## Features

- **AI-powered risk scoring:** `backend/app/services/ai_service.py` calls OpenAI when `OPENAI_API_KEY` is configured and falls back to deterministic heuristics otherwise, producing `risk_score` and `ai_explanation`.
- **Real-time dashboard:** `DashboardPage` aggregates summary cards, severity bar chart, and events-over-time line chart driven by `/stats/summary`.
- **Findings table with pagination & filters:** `FindingsFilters`, `FindingsTable`, and `FindingDetailsModal` in `frontend/src/components/dashboard/` let you filter by severity/user/date range, page through results, view details, and trigger AI enrichment.
- **CORS-enabled backend:** `backend/app/main.py` installs `CORSMiddleware` with permissive defaults so the Vite dev server (port 8080) can hit the FastAPI API (port 8000) without extra configuration.
- **API client + modules:** `frontend/src/api/client.ts` centralizes the base URL (default `http://localhost:8000`, override with `VITE_API_BASE_URL`), and `findings.ts` / `stats.ts` encapsulate the REST calls that power the UI.

## Repository Layout

```
mini-compliance-monitor/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/              # FastAPI routers (health, events, findings, stats)
│   │   ├── core/                     # Configuration helpers (pydantic settings)
│   │   ├── db/                       # Engine, base metadata, dependency helpers
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── ai_service.py          # OpenAI enrichment + fallback heuristics
│   │   │   ├── events_service.py      # SourceEvent filters / pagination
│   │   │   ├── findings_service.py    # Paginated findings queries
│   │   │   ├── stats_service.py       # Summary metrics for the dashboard
│   │   │   ├── ingestion/             # Fake ingestor helpers
│   │   │   ├── log_generator.py       # Synthetic event generator for seeding
│   │   │   └── rules/                 # Rules engine that turns events → findings
│   │   ├── scripts/                   # CLI utilities (seed events, run rules engine)
│   │   └── main.py                    # FastAPI app entrypoint with CORS
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.ts             # Base API client + error handling
│   │   │   ├── findings.ts           # CRUD + AI enrichment calls
│   │   │   └── stats.ts              # Stats summary fetcher
│   │   ├── components/
│   │   │   └── dashboard/            # Summary cards, charts, filters, table, modal
│   │   └── pages/
│   │       └── DashboardPage.tsx     # Dashboard orchestrator
│   ├── vite.config.ts
│   └── package.json
├── docker-compose.yml                # Placeholder (services not wired yet)
└── spec.md                           # Functional specification / roadmap
```

## Prerequisites

- Python 3.11+ (the backend targets 3.12 in CI)
- Node.js 18+ (required for the Vite frontend)
- SQLite (bundled with Python; no separate install needed)
- Optional: Docker & docker-compose for future containerized deployments

## Environment Variables

- `DB_URL` (required) – SQLAlchemy connection string, e.g., `sqlite:///./backend/app/db/app.db`.
- `OPENAI_API_KEY` (optional) – Enables GPT-powered scoring; if absent the backend uses deterministic heuristics.
- `VITE_API_BASE_URL` (optional) – Overrides the frontend’s default `http://localhost:8000`. If you move the backend, point this to the new address before running the dashboard.

The backend loads these variables via `backend/app/core/config.py`, and it looks for a `.env` file in the repo root.

## Backend Setup

1. **Clone & enter the repo**
   ```bash
   git clone <repo-url>
   cd mini-compliance-monitor
   ```
2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Configure environment variables**
   ```bash
   cat <<'EOF' > .env
   DB_URL=sqlite:///./backend/app/db/app.db
   OPENAI_API_KEY=      # optional; remove or leave blank to use heuristics
   EOF
   ```
   This `.env` file is consumed by `pydantic-settings`.
5. **Ensure the SQLite folder exists**
   ```bash
   mkdir -p backend/app/db
   touch backend/app/db/app.db
   ```

## Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```
2. **Start the dev server**
   ```bash
   npm run dev
   ```

The Vite server binds to `::` on port `8080` (see `frontend/vite.config.ts`), so visiting `http://localhost:8080` loads the dashboard.

## Running the Application

### Backend

```bash
PYTHONPATH=backend uvicorn backend.app.main:app --reload
```

- The backend listens on `http://localhost:8000` and exposes the health/events/findings/stats endpoints described below.
- Use `PYTHONPATH=backend` so `import app` works when running from the repo root.

### Frontend

```bash
cd frontend
npm run dev
```

- The dashboard runs on `http://localhost:8080`. It pulls data from `VITE_API_BASE_URL` (defaulting to `http://localhost:8000`).

### Running Both Together

Start the backend command in one terminal, then the frontend command in another (`cd frontend && npm run dev`). The dashboard automatically talks to the API over the permissive CORS middleware.

## API Documentation

- **`GET /health/`**
  - Response: `{ "status": "ok" }`

- **`GET /events/`**
  - Query parameters:
    - `user` – filter by username
    - `event_type` – filter by event type
    - `from_timestamp` / `to_timestamp` – ISO datetimes
    - `limit` (default 50) / `offset` (default 0) – simple pagination
  - Response: `List[SourceEvent]` where each event includes `id`, `event_type`, `user`, `timestamp`, and `raw_data`.

- **`GET /findings/`**
  - Query parameters:
    - `page` (default `1`, min `1`)
    - `page_size` (default `20`, max `100`)
    - `severity`, `user` – equality filters
    - `from_date`, `to_date` – ISO dates (converted to day boundaries)
  - Response: `PaginatedFindings` with `items` (each `Finding` includes `rule_name`, `description`, `severity`, `user`, `created_at`, `risk_score`, and `ai_explanation`), `total`, `page`, and `page_size`.

- **`POST /findings/{finding_id}/enrich_with_ai`**
  - Path parameter: `finding_id`
  - Triggers AI enrichment (OpenAI if configured, otherwise heuristics) and returns the updated `Finding`.

- **`POST /findings/enrich_all_missing`**
  - Query parameter: `limit` (default `50`, max `500`)
  - Enriches all findings without `risk_score` or `ai_explanation` (up to `limit`) and returns the updated list.

- **`GET /stats/summary`**
  - Response: `StatsSummary` with `total_events`, `total_findings`, `findings_by_severity`, and `events_over_time`. This payload powers the dashboard charts.

Visit `http://localhost:8000/docs` for the interactive OpenAPI UI.

## Services

- **`events_service.py`** – Applies filters and pagination to `SourceEvent` rows so `/events/` serves clean timelines.
- **`findings_service.py`** – Converts pagination arguments into limit/offset, adds severity/user/date filters, and structures the result as `items`, `total`, `page`, and `page_size`.
- **`stats_service.py`** – Returns aggregate counts (total events/findings), findings grouped by severity, and daily event counts.
- **`ai_service.py`** – Builds structured prompts, calls OpenAI (if `OPENAI_API_KEY` is set), enforces numeric bounds, and falls back to heuristics that boost scores for sensitive rules. Both single-finding and bulk workflows call this service before committing updates to the DB.

## Data Workflows

| Task | Command | Notes |
| --- | --- | --- |
| Seed fake events | `PYTHONPATH=backend python -m backend.app.scripts.seed_events --n 200` | Generates `n` synthetic `SourceEvent` rows and persists them |
| Run rules engine | `PYTHONPATH=backend python -m backend.app.scripts.run_rules` | Processes new events and inserts normalized findings |

Both scripts lock tables via SQLAlchemy metadata before inserting data.

## Development Workflow

- Start the backend: `PYTHONPATH=backend uvicorn backend.app.main:app --reload`
- Start the frontend: `cd frontend && npm run dev`
- Seed new data or refresh findings before UI demos using the `seed_events` script.
- Re-run the rules engine whenever you add new events or modify detection logic so `findings` stay current.

## Troubleshooting

- **AI enrichment fails with `RuntimeError: OPENAI_API_KEY not configured`:** Either set `OPENAI_API_KEY` in `.env` or rely on the deterministic fallback scores; the frontend gracefully handles either path.
- **`sqlite3.OperationalError: unable to open database file`:** Make sure `backend/app/db` exists and matches the `DB_URL` path. Relative paths resolve from the repo root.
- **`ModuleNotFoundError: No module named 'app'`:** Prefix CLI commands with `PYTHONPATH=backend` or run them from inside `backend/` using the `python -m app...` entrypoint.
- **Dashboard cannot reach API:** Verify `VITE_API_BASE_URL` points to the backend URL (default `http://localhost:8000`) and that the backend is running; cross-origin failures are avoided thanks to `CORSMiddleware` in `backend/app/main.py`.

## Docker & Compose

- `backend/Dockerfile` and `frontend/Dockerfile` describe container boundaries, but the current `docker-compose.yml` is a placeholder and does not wire services yet.

## Contributing

1. Open an issue or jot down enhancements in `spec.md`.
2. Branch from `main`.
3. Keep backend/frontend/infra changes scoped.
4. Run the relevant scripts/tests before opening a PR.

Happy building!

