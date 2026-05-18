# WeGro Agriculture Analytics API — Documentation

This folder contains supporting documentation for the **WeGro Agriculture Analytics API**, built for the WeGro Technologies Limited Associate Data Scientist Technical Assessment.

The root `README.md` explains how to install, run, test, and use the API.  
The files in this `docs/` folder provide deeper technical details about the architecture, API endpoints, data sources, implementation choices, and final submission checklist.

---

## Documentation Index

| Document | Purpose |
|---|---|
| [`../README.md`](../README.md) | Main project guide: setup, Docker, endpoints, testing, and usage |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layered backend architecture, request flow, Docker runtime, and EDA separation |
| [`API_REFERENCE.md`](API_REFERENCE.md) | Endpoint-by-endpoint API reference for all 8 required PRD endpoints |
| [`DATA_GUIDE.md`](DATA_GUIDE.md) | Database views, dimension tables, pandas usage, and EDA notebook context |
| [`PROJECT_REFERENCE.md`](PROJECT_REFERENCE.md) | Project objective, implementation decisions, validation logic, and delivery notes |
| [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) | Final recruiter-facing checklist before submission |

---

## Project Summary

The WeGro Agriculture Analytics API is a production-style FastAPI backend that connects to a remote MySQL agriculture database, processes data using pandas, and exposes 8 analytics endpoints across two reports:

```text
Report 1: Farm Performance Report
Report 2: Crop & Market Intelligence Report
```

The project uses:

```text
FastAPI
pandas
SQLAlchemy
PyMySQL
Pydantic
Docker
```

---

## Required PRD Endpoints

```text
GET /farms/summary
GET /farms/{farm_id}/performance
GET /farms/top
GET /farms/loss-analysis

GET /crops/yield-efficiency
GET /crops/seasonal-trend
GET /markets/price-comparison
GET /crops/quality-breakdown
```

---

## Architecture Asset

The project architecture image is stored inside the documentation assets folder:

```text
docs/assets/Project_Architecture.jpeg
```

It illustrates the main request flow:

```text
External Client
→ FastAPI Application
→ Router Layer
→ Validation & Schema Layer
→ Service Layer
→ Shared pandas Utilities
→ Data Access Layer
→ SQLAlchemy + PyMySQL
→ Remote MySQL Database
```

---

## Runtime Notes

The API is run locally with:

```bash
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker build -t wegro-agriculture-api .
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Testing Notes

Run compile check:

```bash
python -m compileall app scripts
```

Run smoke tests:

```bash
python scripts/check_api_endpoints.py
```

Expected result:

```text
ALL API SMOKE CHECKS PASSED
```

---

## Security Notes

Real database credentials are not committed to GitHub.

The `.env` file is used locally and passed to Docker at runtime:

```bash
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Environment variable names used by this project:

```text
HOST
PORT
USER
PASSWORD
DATABASE
```

---

## Documentation Goal

These documentation files are intended to make the repository easy to review by a recruiter or evaluator.

They explain:

- how the system is structured
- how requests move through the backend
- how pandas analytics are implemented
- how each API endpoint works
- how database sources are used
- how the Docker runtime is configured
- how the final project can be tested locally