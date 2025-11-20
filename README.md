## Mini Compliance Monitor

Mini Compliance Monitor is a full-stack learning project inspired by modern GRC/compliance platforms. It ingests security/log events, runs rule-based detections, and exposes REST APIs plus a future React dashboard so you can demonstrate backend, data, and DevOps fundamentals in one place.

### Key Capabilities

- FastAPI backend with SQLAlchemy models for `SourceEvent` and `Finding`
- Ingestion utilities for generating or importing log data
- Rules engine that scans normalized events and emits findings
- Stats endpoints for dashboard visualizations
- Planned React + TypeScript frontend and Dockerized deployment targets

## Repository Layout

```
mini-compliance-monitor/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (health, events, findings, stats)
│   │   ├── core/         # Settings / configuration helpers
│   │   ├── db/           # SQLAlchemy engine, base, dependencies
│   │   ├── models/       # ORM models
│   │   ├── schemas/      # Pydantic response models
│   │   ├── scripts/      # CLI utilities (seed events, run rules)
│   │   └── services/     # Ingestion + rules logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/              # React dashboard (scaffold)
│   └── Dockerfile
├── docker-compose.yml    # Multi-service runtime (stub)
└── spec.md               # Functional specification / roadmap
```

## Prerequisites

- Python 3.11+ (project developed on 3.12)
- Node.js 18+ (for the future frontend)
- SQLite (bundled with Python; no separate install needed)
- Optional: Docker & docker-compose

## Backend Setup

1. **Clone & enter the repo**
   ```bash
   git clone <repo-url>
   cd mini-compliance-monitor
   ```
2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Environment variables**
   - Create `backend/.env` (or copy the example once it exists) with at least:
     ```
     DB_URL=sqlite:///./backend/app/db/app.db
     ```
   - The settings loader expects the `.env` file at the repo root when you run commands from `mini-compliance-monitor/`.
5. **Ensure the SQLite path exists**
   ```bash
   mkdir -p backend/app/db
   touch backend/app/db/app.db
   ```

## Running the Backend API

From the repo root:

```bash
PYTHONPATH=backend uvicorn backend.app.main:app --reload
```

- The `PYTHONPATH=backend` prefix ensures `app.*` imports resolve when running from the root.
- The API exposes:
  - `GET /health/`
  - `GET /events/`
  - `GET /findings/`
  - `GET /stats/summary`

Visit `http://127.0.0.1:8000/docs` for the interactive OpenAPI explorer.

## Data Workflows

| Task | Command (run from repo root) | Notes |
| --- | --- | --- |
| Seed fake events | `PYTHONPATH=backend python -m backend.app.scripts.seed_events --n 200` | Generates `n` synthetic `SourceEvent` rows and persists them |
| Run rules engine | `PYTHONPATH=backend python -m backend.app.scripts.run_rules` | Processes unprocessed events and inserts new findings |

Both scripts will auto-create tables via SQLAlchemy metadata if they do not exist yet.

## Frontend (planned)

The frontend scaffold lives under `frontend/` and will eventually host a React + TypeScript dashboard. Until the UI is implemented, you can create a new app with Vite or Next.js and point its API client at the FastAPI backend.

## Docker & Compose

- `backend/Dockerfile` and `frontend/Dockerfile` outline container boundaries (build steps still TBD).
- `docker-compose.yml` is reserved for orchestrating the API, frontend, and a production-grade database service.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'app'`**  
  Prefix commands with `PYTHONPATH=backend` (or run them from `backend/` using `python -m app.<module>`).
- **`sqlite3.OperationalError: unable to open database file`**  
  Ensure the directory referenced in `DB_URL` exists and that you are running commands from the repo root so relative paths resolve correctly.
- **FastAPI serialization errors on stats endpoints**  
  Return JSON-friendly dicts/lists (not raw SQLAlchemy tuples) when extending routes.

## Contributing

1. Open an issue or note the enhancement in `spec.md`.
2. Create a feature branch.
3. Keep changes isolated (backend, frontend, infra as needed).
4. Run relevant scripts/tests before opening a PR.

Happy building!

