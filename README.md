# AI Threat Detection System

A multi-service system that ingests HTTP request logs, detects suspicious activity through both rule-based and machine-learning detectors, and uses Claude to generate plain-language explanations of what was found, all viewable through a small React dashboard.

## Architecture

Five services, each independently containerized, sharing one alert store:

```
log_generator.py ──POST /logs──▶ ingestion-service (FastAPI, :8001) ──SQLite──▶ logs + alerts
                                        ▲                    ▲
                                        │                    │
                          rule-engine (Java) ──┐    ml-engine (Python) ──┐
                          polls /logs, posts    │    polls /logs, posts   │
                          to /alerts            │    to /alerts           │
                                                 └──────────┬─────────────┘
                                                             ▼
                                              frontend (React, :5173) ── displays alerts
                                                             │
                                                             ▼
                                              ai-reasoning (:8002) ── on click, explains
                                              one alert via the Claude API
```

- **ingestion-service**: receives and stores logs and alerts (FastAPI + SQLite)
- **rule-engine** (Java): six deterministic detection rules (brute-force login, credential stuffing, port scanning, unusual endpoint access), polling every 5 seconds
- **ml-engine** (Python): an Isolation Forest (unsupervised anomaly detection) plus a Random Forest (labels *what kind* of anomaly), trained on synthetic data
- **ai-reasoning** (Python/FastAPI): on demand, fetches one alert and asks Claude to explain it in plain language
- **frontend** (React + TypeScript): a dashboard listing alerts with an "Explain" button per row

Rule-engine and ml-engine are two independent detectors that both feed the same `/alerts` store, neither depends on the other to work.

## Running it

**Prerequisite:** to use the AI explain feature, you need an Anthropic API key. Create `backend/ai-reasoning/.env`:
```
ANTHROPIC_API_KEY=your-key-here
```
(Everything else works without this, logs, rules, and ML detection all run independently of it.)

**Start everything:**
```
docker compose up --build
```
Then open `http://localhost:5173` for the dashboard. First build takes a few minutes; subsequent ones are much faster thanks to Docker's layer caching.

**Generate some traffic to see it work:**
```
python backend/scripts/log_generator.py
```

**Stop everything:**
```
docker compose down
```
(Alert/log data persists in a Docker volume across restarts, use `docker compose down -v` if you want a completely clean slate.)

## Local development (without Docker)

Each service can also run standalone for development:

- **ingestion-service:** `cd backend/ingestion-service/app && uvicorn main:app --reload --port 8001`
- **rule-engine:** `cd backend/rule-engine && mvn exec:java` (or `./run.ps1` on Windows)
- **ml-engine:** `cd backend/ml-engine && python -m inference.score_logs`
- **ai-reasoning:** `cd backend/ai-reasoning && uvicorn main:app --reload --port 8002`
- **frontend:** `cd frontend && npm run dev`

Each Python service has its own `requirements.txt`.

## Limitations

- Log data is synthetic (`log_generator.py`), no real application traffic is ingested by default
- Alert deduplication is in-memory per detector process and resets on restart
- ml-engine is trained on synthetic data generated on the fly; its per-class evaluation numbers are illustrative, not large-sample statistically rigorous
