# Mini Compliance Monitor

Mini Compliance Monitor is a fully functional, realistic mini GRC (Governance, Risk & Compliance) platform inspired by Anecdotes. The project demonstrates backend engineering, rule-based detection, AI-powered enrichment, log ingestion, analytics, and a full React dashboard.

---

## 1. Project Overview

### Purpose

To build a small but realistic compliance monitoring system that:

- Ingests raw security/activity events
- Normalizes and stores them
- Processes them with a Rules Engine
- Generates Findings (alerts)
- Enriches Findings with AI (risk score + explanation)
- Visualizes everything in a modern dashboard
- Can be deployed easily (Docker, Render, Railway, Fly.io)

### Audience

- Recruiters evaluating backend/full-stack/AI skills
- A hands-on learning platform for understanding real GRC systems

---

## 2. Main Use Case

> “As a security/compliance engineer, I want to monitor suspicious or risky activity across my systems, based on ingested logs, so I can detect potential issues early.”

### Flow

1. Raw events are generated (fake logs) or ingested from external sources
2. Normalized into `SourceEvent` records
3. Rules Engine evaluates events and produces `Findings`
4. AI Engine enriches Findings with `risk_score` + `ai_explanation`
5. Dashboard displays statistics, charts, and detailed findings
6. User can manually or batch-enrich findings with AI

---

## 3. System Architecture

**Backend (FastAPI)**

- API routes (`health`, `events`, `findings`, `stats`)
- SQLAlchemy models + schemas
- Ingestion & log generation services
- Rules engine that emits findings
- Stats + AI enrichment services

**Database**

- SQLite (development)
- PostgreSQL planned in the future

**Frontend (React + TypeScript + Tailwind + shadcn/ui)**

- Dashboard aggregating metrics, charts, filters, and tables
- Summary cards, findings table, and AI enrichment tools
- Vite dev server with TanStack Query + React Router

**DevOps**

- Docker & docker-compose (placeholder)
- Deployable to Render, Railway, Fly.io

---

## 4. Data Model

### 4.1 `source_events`

| Field           | Type       | Description                                    |
|-----------------|------------|------------------------------------------------|
| `id`            | int (PK)   | Unique event ID                                |
| `timestamp`     | datetime   | When the event occurred                         |
| `user`          | string     | Actor/user                                      |
| `event_type`    | string     | e.g., `login_failed`, `api_token_created`      |
| `raw_data`      | JSON       | Original payload (IPs, change counts, scopes)  |
| `processed`     | boolean   | Whether the Rules Engine has processed it       |

#### Supported Event Types

- **Auth**: `login_success`, `login_failed`
- **MFA**: `mfa_challenge`, `mfa_failed`, `mfa_success`
- **Git**: `pull_request_opened`, `pull_request_merged`
- **Permissions**: `permission_changed`
- **API Tokens**: `api_token_created`, `api_token_revoked`
- **Deployments**: `deployment_started`, `deployment_succeeded`, `deployment_failed`
- **Storage**: `storage_bucket_created`, `storage_bucket_permission_changed`

Each event includes rich `raw_data` such as repository metadata, location, change counts, scopes, and visibility flags.

### 4.2 `findings`

| Field           | Type     | Description                            |
|-----------------|----------|----------------------------------------|
| `id`            | int (PK) | Finding ID                               |
| `rule_name`     | string   | Rule that triggered                      |
| `description`   | string   | Human-readable explanation               |
| `severity`      | enum     | `low`, `medium`, `high`, `critical`     |
| `user`          | string   | Associated user                          |
| `created_at`    | datetime | Auto timestamp                            |
| `event_id`      | FK       | Related `source_event` (optional)      |
| `risk_score`    | float    | 0–100 AI risk assessment                 |
| `ai_explanation` | string   | AI-generated explanation                 |
| `extra_data`    | JSON     | Optional metadata                        |

---

## 5. API Specification

### Base path: `/`

### 5.1 Health Check

`GET /health`

**Response**

```json
{ "status": "ok" }
```

### 5.2 Events

`GET /events`

**Query parameters**

- `user` – filter by user
- `event_type` – filter by event type
- `from_timestamp` / `to_timestamp` – ISO 8601 datetimes
- `limit` (default `50`) / `offset` (default `0`)

**Response**

`List[SourceEvent]` objects with `id`, `event_type`, `user`, `timestamp`, and `raw_data`.

### 5.3 Findings

`GET /findings`

**Query parameters**

- `page` (default `1`, min `1`)
- `page_size` (default `20`, max `100`)
- `severity`, `user` – equality filters
- `from_date`, `to_date` – ISO dates converted to day boundaries

**Response**

`PaginatedFindings`:

- `items` – each `Finding` (includes `rule_name`, `description`, `severity`, `user`, `created_at`, `risk_score`, and `ai_explanation`)
- `total`, `page`, `page_size`

### 5.4 AI Enrichment

#### Enrich a single finding

`POST /findings/{finding_id}/enrich_with_ai`

- Path: `finding_id`
- Returns the updated `Finding`
- Uses OpenAI if `OPENAI_API_KEY` is configured, otherwise fallback heuristics

#### Batch enrichment

`POST /findings/enrich_all_missing`

- Query: `limit` (default `50`, max `500`)
- Enriches findings missing `risk_score` or `ai_explanation`
- Returns the list of updated findings

### 5.5 Stats Summary

`GET /stats/summary`

**Response**

```json
{
  "total_events": 1234,
  "total_findings": 45,
  "findings_by_severity": {
    "low": 10,
    "medium": 20,
    "high": 15,
    "critical": 12
  },
  "events_over_time": [
    { "date": "2025-01-20", "count": 100 },
    { "date": "2025-01-21", "count": 150 }
  ]
}
```

Drives the dashboard cards, bar chart, and event timeline.

---

## 6. Ingestion Layer

### 6.1 Fake Log Generator

- Generates hundreds of realistic events with randomized users and rich `raw_data`
- Distributes events across ~30 days with varied timestamps
- Exposes helpers:
  - `generate_fake_event()`
  - `generate_fake_events_batch(n)`
  - `save_events_to_db(events)`

### 6.2 GitHub Integration (Future)

- `fetch_github_events(since)`
- `normalize_github_event(event)`
- Potential sources: GitHub Events API, GitHub Audit Log API

---

## 7. Rules Engine

**Core function**

- `apply_rules_to_event(event, db) -> list[Finding]`

**Rule categories**

- **Authentication**
  - Too many login failures → medium/high/critical
  - Suspicious login after failures → critical
- **MFA**
  - Repeated failures → medium/high
  - Success following failures → low
- **Permissions**
  - Role escalation to admin → high/critical
  - Viewer → developer escalation → medium
- **API Tokens**
  - `admin:*` → critical
  - Missing expiry → high
- **Git / PR**
  - Large merge (>400 lines) → high
  - Medium-sized changes → medium
- **Deployments**
  - Failure in prod → high
  - Failure in staging → medium
- **Storage**
  - Public bucket detected → critical
- **Global activity**
  - Too many events in the last hour → high

**Execution script**

- `python -m app.scripts.run_rules`
- Fetches unprocessed events, applies rules, inserts findings, marks events as processed

---

## 8. Frontend (React + TypeScript + Tailwind + shadcn/ui)

**Features**

- Modern dashboard UI (Lovable-generated + manual polish)
- Summary cards for top-level counts
- Severity bar chart + events-over-time line chart (Recharts)
- Rich findings table with:
  - Severity badges
  - Risk score column
  - AI column (Enrich with AI / Enriched)
  - Responsive, scrollable layout (`min-w-[1100px]`)
- Batch enrichment button: “Enrich All with AI”

**API client**

- `getSummary()`
- `getFindings()`
- `enrichFinding()`
- `enrichAllMissing()`

---

## 9. Non-Functional Requirements

- Clean, readable, maintainable code
- No authentication in the MVP
- Easy to extend rules, log sources, integrations
- SQLite for fast local development
- Container-ready architecture

---

## 10. Future Enhancements

- Migrate to PostgreSQL + Alembic migrations
- Add log sources: AWS CloudTrail, Okta, Azure AD
- Explore AI anomaly detection models
- Expand dashboards: user-, event-, rule-level views
- Plugin system for custom rules
- RBAC (roles & authentication)
- CI/CD pipeline

---

## Summary

The Mini Compliance Monitor is now a fully working, end-to-end compliance monitoring system with:

- Log ingestion
- Normalized storage
- A rich Rules Engine
- AI-powered enrichment
- Full dashboard UI
- Batch processing
- Extendable architecture

Perfect for portfolios, interviews, and practical GRC learning.