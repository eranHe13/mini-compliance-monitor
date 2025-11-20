## 1. Project Name, Purpose, and Audience

Project Name:
Mini Compliance Monitor

Primary Goal:
Build a small but realistic GRC/Compliance-like system (inspired by Anecdotes) that demonstrates:

- 1.Backend development (FastAPI, SQL, API design)
- Log ingestion & data normalization
- Rules Engine + optional AI/ML
- React dashboard with charts, filters, findings
- Containerization + easy deployment (Docker + Render/Fly.io/Railway)

Who Is This For?

- Recruiters looking at your full-stack/backend skills
- You, as a practical hands-on learning project for GRC systems

## 2. Main Use Case

“As a security/compliance engineer, I want to view suspicious or risky activity across my systems, based on ingested log data, so I can detect potential issues early.”

Flow:

- System ingests raw events (fake logs or real GitHub API).
- Events are normalized and stored in the DB.
- Rules Engine analyzes events and generates Findings.
- Dashboard displays counts, severity, activity trends, and a table of findings.

## 3. High-Level Architecture

Components

- Backend (Python + FastAPI)
  - API layer
  - DB models (SQLAlchemy)
  - Ingestion services
  - Rules Engine
  - Stats module
- Database
  - SQLite (development)
  - PostgreSQL (optional later)
- Log Sources
  - Phase 1: Fake Log Generator
  - Phase 2: Real integration (GitHub events / audit logs)
- Frontend (React + TypeScript)
  - Dashboard
  - Charts
  - Filters
  - Findings table
- DevOps
  - Docker
  - docker-compose
  - Deployment to Render / Railway / Fly.io

## 4. Data Model

### 4.1 Table: source_events

Represents raw ingested events.

Fields:

- id – primary key
- external_id – ID from external source (nullable for fake logs)
- source – "fake" or "github"
- timestamp – event timestamp
- user – actor/username
- event_type – e.g., "login_failed", "pull_request_opened"
- severity_hint – optional (initial categorization)
- raw_data – full JSON payload
- processed – boolean, whether event has been analyzed

### 4.2 Table: findings

Represents alerts/anomalies created by the rules engine.

Fields:

- id – primary key
- rule_name – name of the rule that triggered
- severity – "low" | "medium" | "high" | "critical"
- description – human-readable explanation
- timestamp – creation time
- user – associated user (if relevant)
- event_id – FK → source_events.id (optional)
- risk_score – 0–100 numeric risk (future AI)
- extra_data – JSON metadata related to the detection

## 5. API Specification

All routes under /api.

### 5.1 Health

GET /api/health

Returns:

{ "status": "ok" }

### 5.2 Events

GET /api/events

Query params (all optional):

- user
- event_type
- from, to
- limit, offset

Response: list of SourceEvent.

(Optional) POST /api/events

Allows manual creation (useful for demo).

### 5.3 Findings

GET /api/findings

Query params:

- severity
- user
- rule_name
- from, to
- limit, offset

Response: list of Finding.

### 5.4 Stats / Dashboard Data

GET /api/stats/summary

Returns:

```
{
  "total_events": 1234,
  "total_findings": 45,
  "findings_by_severity": {
    "low": 10,
    "medium": 20,
    "high": 15
  },
  "events_over_time": [
    { "date": "2025-01-20", "count": 100 },
    { "date": "2025-01-21", "count": 150 }
  ],
  "findings_over_time": [
    { "date": "2025-01-20", "count": 5 },
    { "date": "2025-01-21", "count": 8 }
  ]
}
```

## 6. Ingestion Layer

### 6.1 Phase 1 — Fake Logs

Module: app/services/fake_ingestion.py

Functions:

- generate_fake_event()
- generate_fake_events_batch(n)
- save_events_to_db(events)

Event types:

- login_success
- login_failed
- pull_request_opened
- pull_request_merged
- role_changed

Users generated randomly from a small predefined pool.
Timestamps randomized across a defined range.

### 6.2 Phase 2 — GitHub Integration

Module: app/services/github_client.py

Functions:

- fetch_github_events(since)
- normalize_github_event(event)

Log sources:

- GitHub events API
- GitHub audit-log API (if needed)

Normalized into the SourceEvent structure.

## 7. Rules Engine

Module: app/services/rules_engine.py

### 7.1 Rule Structure

Simple functional approach:

```
def rule_login_failed(events) -> list[Finding]:
    ...

def rule_high_activity(events) -> list[Finding]:
    ...
```

Or a class-based interface.

### 7.2 MVP Rules

Rule 1 — Login Failed → High Severity

If event_type = "login_failed" → generate high-severity finding.

Rule 2 — High Activity

If user has >N events within a short time window → generate medium severity finding.

Rule 3 — Rare Event Type (optional)

Event type occurs rarely → lower severity finding.

### 7.3 Rule Execution

Function:
run_rules_on_new_events()

Steps:

1. Fetch unprocessed events
2. Run all rules
3. Insert generated findings
4. Mark events as processed

Execution mode:

- Script (python -m app.scripts.run_rules)
- Or scheduled job

## 8. Frontend Specification (React + TypeScript)

Tech stack:

- React
- TypeScript
- TailwindCSS
- Recharts / Chart.js

### 8.1 Main Pages

Dashboard

Sections:

- Summary cards (events, findings, breakdown by severity)
- Activity charts
- Findings table with filters

### 8.2 Components

- DashboardPage
- StatsCards
- EventsChart
- FindingsChart
- FindingsTable (sortable + filterable)

### 8.3 API Client

Module src/api/client.ts:

- getSummary()
- getFindings(params)
- getEvents(params)

## 9. Non-Functional Requirements

- Code clarity: readable, simple, maintainable
- No authentication in MVP
- Small to moderate dataset

Documentation:

- README with instructions
- Screenshots

Extensibility:

- Add more log sources
- Add more rules
- Enhance AI/ML

## 10. Future Enhancements

- Switch to PostgreSQL + Alembic
- Add more integrations (AWS CloudTrail, Azure, etc.)
- Add advanced AI (LLM scoring, anomaly models)
- Drill-down screens (per user, per event)
- Plugins-based architecture for rules