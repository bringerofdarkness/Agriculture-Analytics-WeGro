# WeGro Agriculture Analytics API

A production-ready FastAPI analytics backend built for the **WeGro Technologies Limited Associate Data Scientist Technical Assessment**.

This project connects to a remote MySQL agriculture database, processes agriculture data with **pandas**, and exposes **8 required analytics endpoints** across two business reports:

1. Farm Performance Report  
2. Crop & Market Intelligence Report  

The project focuses on correctness, clean architecture, recruiter-friendly documentation, strong API validation, professional error handling, and Docker-based deployment readiness.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Assessment Goal](#assessment-goal)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Database Sources](#database-sources)
- [Environment Variables](#environment-variables)
- [Run Locally](#run-locally)
- [Run with Docker](#run-with-docker)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Accepted Filter Values](#accepted-filter-values)
- [Important Season Handling Note](#important-season-handling-note)
- [Example Requests](#example-requests)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Implementation Notes](#implementation-notes)
- [Final Submission Checklist](#final-submission-checklist)

---

## Project Overview

The WeGro Agriculture Analytics API is a backend data product that transforms raw agriculture database records into clean, filterable business insights.

It uses:

- **SQLAlchemy** for database connectivity
- **PyMySQL** for MySQL access
- **pandas** for analytics and aggregation
- **FastAPI** for REST API development
- **Pydantic** for response validation
- **Docker** for containerized deployment

The API is designed to be tested locally by evaluators through Swagger UI, curl, Postman, or direct browser/API requests.

---

## Assessment Goal

The assessment goal is to:

> Connect to a MySQL agriculture database, process the data using Python and pandas, and serve the analytics through a FastAPI web API with 8 endpoints across 2 reports.

This implementation prioritizes:

- correct database usage
- clean pandas processing
- complete endpoint coverage
- strict request validation
- correct JSON response shape
- meaningful API errors
- readable and maintainable code
- Docker deployment support

---

## Key Features

- 8 PRD-required FastAPI endpoints
- Remote MySQL database connection
- SQLAlchemy engine setup
- pandas-based filtering, joining, grouping, and aggregation
- Enum-based query/path validation
- Strict Pydantic response schemas
- Clean route-service-schema architecture
- Professional 404 responses for valid filters with no matching rows
- Professional 422 responses for invalid filter values
- Swagger/OpenAPI documentation
- Multi-stage Dockerfile
- Non-root Docker runtime user
- Local smoke test script for endpoint verification

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| API Framework | FastAPI |
| API Server | Uvicorn |
| Data Processing | pandas |
| Database | MySQL |
| DB Connection | SQLAlchemy + PyMySQL |
| Validation | Pydantic |
| Environment Config | python-dotenv / Pydantic Settings |
| Containerization | Docker |
| API Docs | Swagger UI / OpenAPI |

---

## Project Architecture

```text
WeGro/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   │
│   ├── enums/
│   │   ├── __init__.py
│   │   └── filters.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── farms.py
│   │   ├── crops.py
│   │   ├── markets.py
│   │   └── crop_quality.py
│   │
│   ├── schemas/
│   │   ├── filters.py
│   │   ├── farm_reports.py
│   │   ├── crop_reports.py
│   │   └── market_reports.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── dataframe_utils.py
│       ├── farm_reports.py
│       ├── crop_reports.py
│       └── market_reports.py
│
├── scripts/
│   ├── check_api_endpoints.py
│   ├── check_all_endpoints.py
│   ├── check_crop_quality_breakdown.py
│   └── check_market_price_comparison.py
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## Database Sources

The project uses the provided MySQL agriculture database.

Recommended database views used:

```text
vw_harvest_full
vw_revenue_by_crop_year
vw_farm_profitability
```

Dimension tables used where needed:

```text
dim_farm
dim_crop
dim_market
```

Examples:

- `dim_farm` is used to validate `farm_id` and fetch farm metadata.
- `dim_crop` is used for crop benchmark yield, crop ID filtering, and growing season.
- `dim_market` is used for correct market district and price tier analysis.
- `vw_harvest_full` is used as the main harvest and sales analytics source.

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DB_HOST=your_mysql_host
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=agriculture_db
```

The `.env` file is intentionally excluded from Git and Docker build context.

Do not commit database credentials to GitHub.

---

## Run Locally

### 1. Clone the repository

```bash
git clone <your-public-github-repo-url>
cd WeGro
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the root directory and add the database credentials provided for the assessment.

### 5. Start the API server

```bash
uvicorn app.main:app --reload
```

The server will run at:

```text
http://127.0.0.1:8000
```

---

## Run with Docker

### 1. Build the Docker image

```bash
docker build -t wegro-agriculture-api .
```

### 2. Run the container

```bash
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

The containerized API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

After starting the server, open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON is available at:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger UI can be used to test all endpoints and inspect request/response schemas.

---

## API Endpoints

### Report 1: Farm Performance Report

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | GET | `/farms/summary` | Returns farm-level revenue, cost, profit, and average loss summary |
| 2 | GET | `/farms/{farm_id}/performance` | Returns detailed performance for a single farm |
| 3 | GET | `/farms/top` | Returns top farms ranked by profit, revenue, or yield |
| 4 | GET | `/farms/loss-analysis` | Returns post-harvest loss analysis by region, crop category, quality grade, and pesticide residue |

### Report 2: Crop & Market Intelligence Report

| # | Method | Endpoint | Description |
|---|---|---|---|
| 5 | GET | `/crops/yield-efficiency` | Compares actual crop yield against benchmark yield |
| 6 | GET | `/crops/seasonal-trend` | Shows seasonal revenue and quantity trend by crop |
| 7 | GET | `/markets/price-comparison` | Compares crop selling prices across markets, districts, and price tiers |
| 8 | GET | `/crops/quality-breakdown` | Shows crop quality grade and pesticide residue distribution |

---

## Accepted Filter Values

| Filter | Accepted Values |
|---|---|
| `region` | Dhaka, Chittagong, Sylhet, Rajshahi, Khulna, Rangpur, Barisal, Mymensingh |
| `farm_type` | Small, Medium, Large, Commercial |
| `crop_category` | Cereal, Vegetable, Fruit, Pulse, Oilseed, Cash Crop, Spice |
| `season` | Spring, Summer, Autumn, Winter |
| `growing_season` / crop season | Rabi, Kharif, Zaid, Year-Round |
| `market_type` | Local, Wholesale, Export, Retail, Government Procurement |
| `price_tier` | Low, Medium, High, Premium |
| `quality_grade` | A, B, C, D |
| `pesticide_residue` | None, Trace, Low, High |
| `water_requirement` | Low, Medium, High |
| `year` | 2022, 2023, 2024 |
| `quarter` | 1, 2, 3, 4 |
| `metric` | profit, revenue, yield |
| `limit` | Any positive integer. Default: 10 |

---

## Important Season Handling Note

Most PRD endpoints use calendar or harvest season values:

```text
Spring, Summer, Autumn, Winter
```

However, the following endpoints analyse crop-growing behaviour and therefore use crop growing season values:

```text
Rabi, Kharif, Zaid, Year-Round
```

Affected endpoints:

```text
/farms/loss-analysis
/crops/yield-efficiency
```

This distinction is important because the database contains both calendar season and crop growing season concepts.

---

## Example Requests

### 1. Farm Summary

```bash
curl "http://127.0.0.1:8000/farms/summary"
```

```bash
curl "http://127.0.0.1:8000/farms/summary?region=Dhaka&year=2023"
```

---

### 2. Single Farm Performance

```bash
curl "http://127.0.0.1:8000/farms/1/performance"
```

```bash
curl "http://127.0.0.1:8000/farms/1/performance?year=2023&crop_category=Cereal&market_type=Wholesale"
```

---

### 3. Top Farms Ranking

```bash
curl "http://127.0.0.1:8000/farms/top"
```

```bash
curl "http://127.0.0.1:8000/farms/top?metric=profit&region=Rajshahi&limit=5"
```

---

### 4. Loss Analysis

```bash
curl "http://127.0.0.1:8000/farms/loss-analysis"
```

```bash
curl "http://127.0.0.1:8000/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A"
```

---

### 5. Crop Yield Efficiency

```bash
curl "http://127.0.0.1:8000/crops/yield-efficiency"
```

```bash
curl "http://127.0.0.1:8000/crops/yield-efficiency?crop_category=Vegetable&year=2023&region=Dhaka"
```

---

### 6. Seasonal Revenue Trend

```bash
curl "http://127.0.0.1:8000/crops/seasonal-trend"
```

```bash
curl "http://127.0.0.1:8000/crops/seasonal-trend?crop_category=Vegetable&year=2023"
```

---

### 7. Market Price Comparison

```bash
curl "http://127.0.0.1:8000/markets/price-comparison"
```

```bash
curl "http://127.0.0.1:8000/markets/price-comparison?crop_category=Cereal&year=2023&market_type=Export"
```

---

### 8. Quality Grade Breakdown

```bash
curl "http://127.0.0.1:8000/crops/quality-breakdown"
```

```bash
curl "http://127.0.0.1:8000/crops/quality-breakdown?crop_category=Fruit&year=2023&region=Rajshahi"
```

---

## Testing

### Compile check

```bash
python -m compileall app scripts
```

### Endpoint smoke test

```bash
python scripts/check_api_endpoints.py
```

Expected output:

```text
ALL API SMOKE CHECKS PASSED
```

The smoke test checks:

- all 8 successful endpoint responses
- invalid path/query validation
- 422 validation responses
- 404 no-data responses

---

## Error Handling

The API returns structured error responses.

### Invalid filter value

Example:

```bash
curl "http://127.0.0.1:8000/farms/summary?region=InvalidCity"
```

Expected status:

```text
422 Unprocessable Entity
```

### Valid filter value but no matching data

Example:

```bash
curl "http://127.0.0.1:8000/markets/price-comparison?district=UnknownDistrict"
```

Expected status:

```text
404 Not Found
```

Example response shape:

```json
{
  "error": "Data not found",
  "message": "No matching data found for the requested filters.",
  "hint": "Your filter values are valid, but no database rows matched them. Try removing or broadening one or more filters.",
  "path": "/example-path",
  "status_code": 404
}
```

---

## Implementation Notes

### Farm Summary

The farm summary endpoint aggregates revenue, input cost, net profit, and post-harvest loss percentage by farm.

### Single Farm Performance

The single farm performance endpoint validates `farm_id` using `dim_farm`, maps it to the farm name, and then filters harvest performance records.

### Top Farms Ranking

The top farms endpoint supports ranking by:

```text
profit
revenue
yield
```

The default metric is `profit`, and the default limit is `10`.

### Loss Analysis

The loss analysis endpoint uses crop growing season values such as:

```text
Rabi, Kharif, Zaid, Year-Round
```

It calculates total harvested quantity, total lost quantity, overall loss percentage, and grouped loss breakdowns.

### Crop Yield Efficiency

Actual yield is calculated as:

```text
actual_avg_yield_ton_per_ha = quantity_harvested_ton / area_planted_ha
```

Benchmark yield comes from:

```text
dim_crop.avg_yield_ton_per_ha
```

Efficiency is calculated as:

```text
efficiency_pct = actual_avg_yield_ton_per_ha / avg_yield_benchmark_ton_per_ha * 100
```

Some crops may show exactly `100%` efficiency because the sample database contains benchmark-aligned harvest records.

### Seasonal Revenue Trend

The seasonal trend endpoint groups crop revenue and quantity sold by crop, year, quarter, and season.

### Market Price Comparison

The market price endpoint joins market metadata so that district and price tier come from `dim_market`, not farm district.

### Quality Grade Breakdown

The quality breakdown endpoint returns:

- total record count
- grade distribution for A, B, C, D
- pesticide residue breakdown for None, Trace, Low, High

---

## Docker Notes

The Dockerfile uses a multi-stage build:

1. Builder stage installs compile-time dependencies and Python packages.
2. Runtime stage copies only the prepared virtual environment and application code.
3. The container runs with a non-root `appuser`.

This keeps the final image cleaner and safer than a single-stage build.

---

## Final Submission Checklist

Before submitting the GitHub repository:

- [ ] All 8 endpoints return successful responses
- [ ] Invalid filters return 422
- [ ] Valid filters with no matching rows return 404
- [ ] `python -m compileall app scripts` passes
- [ ] `python scripts/check_api_endpoints.py` passes
- [ ] `requirements.txt` is present
- [ ] `README.md` explains how to run locally
- [ ] `Dockerfile` is present
- [ ] Docker image builds successfully
- [ ] Docker container runs successfully
- [ ] `.env` is not committed
- [ ] Git working tree is clean
- [ ] Repository is public before submission

---

## Submission

This repository is prepared for the WeGro Technologies Limited Associate Data Scientist Technical Assessment.

The API can be run locally or through Docker, and all required PRD endpoints are available through Swagger UI at:

```text
http://127.0.0.1:8000/docs
```