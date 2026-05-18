# WeGro Agriculture Analytics API

A FastAPI-based agriculture analytics backend built for the **WeGro Technologies Limited Associate Data Scientist Technical Assessment**.

The API connects to a remote MySQL agriculture database, processes data with pandas, and exposes 8 analytics endpoints for farm performance, crop yield, market pricing, seasonal trends, loss analysis, and crop quality breakdown.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/bringerofdarkness/Agriculture-Analytics-WeGro.git
cd Agriculture-Analytics-WeGro
```

---

### 2. Create Environment File

Create a `.env` file in the project root:

```env
HOST=your_mysql_host
PORT=3306
USER=your_mysql_username
PASSWORD=your_mysql_password
DATABASE=agriculture_db
```

The `.env` file is not committed to GitHub.

---

### 3. Run Locally

Create and activate virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API server:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Run with Docker

Build the Docker image:

```powershell
docker build -t wegro-agriculture-api .
```

Run the container:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Verify the Project

Run compile check:

```powershell
python -m compileall app scripts
```

Run automated API smoke test:

```powershell
python scripts\check_api_endpoints.py
```

Expected final output:

```text
ALL API SMOKE CHECKS PASSED
```

The smoke test verifies:

```text
8 successful endpoint responses
422 validation cases
404 no-data cases
```

---

## API Overview

Base URL:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Required Endpoints

### Farm Performance Report

| # | Method | Endpoint | Purpose |
|---|---|---|---|
| 1 | GET | `/farms/summary` | Farm revenue, cost, profit, and loss summary |
| 2 | GET | `/farms/{farm_id}/performance` | Detailed performance for one farm |
| 3 | GET | `/farms/top` | Top farms ranked by profit, revenue, or yield |
| 4 | GET | `/farms/loss-analysis` | Post-harvest loss analysis |

### Crop & Market Intelligence Report

| # | Method | Endpoint | Purpose |
|---|---|---|---|
| 5 | GET | `/crops/yield-efficiency` | Actual crop yield vs benchmark yield |
| 6 | GET | `/crops/seasonal-trend` | Seasonal revenue and quantity trends |
| 7 | GET | `/markets/price-comparison` | Market price comparison by crop and market |
| 8 | GET | `/crops/quality-breakdown` | Quality grade and pesticide residue distribution |

For detailed request examples, response contracts, and validation behavior, see:

```text
docs/API_PLAYBOOK.md
```

[Open API Playbook](docs/API_PLAYBOOK.md)

---

## Example Requests

### Farm Summary

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/summary?region=Dhaka&year=2023" | ConvertTo-Json -Depth 10
```

### Single Farm Performance

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/1/performance?year=2023&crop_category=Cereal" | ConvertTo-Json -Depth 10
```

### Top Farms

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=profit&limit=5" | ConvertTo-Json -Depth 10
```

### Loss Analysis

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A" | ConvertTo-Json -Depth 10
```

### Crop Yield Efficiency

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/yield-efficiency?crop_category=Vegetable&year=2023&region=Dhaka" | ConvertTo-Json -Depth 10
```

### Seasonal Revenue Trend

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/seasonal-trend?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

### Market Price Comparison

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?district=Chittagong" | ConvertTo-Json -Depth 10
```

### Quality Grade Breakdown

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/quality-breakdown?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

---

## Technology Stack

| Area | Tool |
|---|---|
| API Framework | FastAPI |
| Server | Uvicorn |
| Data Processing | pandas |
| Database | MySQL |
| Database Access | SQLAlchemy + PyMySQL |
| Validation | Pydantic |
| Runtime | Python 3.11 |
| Deployment | Docker |

---

## Project Structure

```text
app/
  main.py
  config.py
  database.py
  exceptions.py

  enums/
    filters.py

  routers/
    farms.py
    crops.py
    markets.py
    crop_quality.py

  schemas/
    filters.py
    farm_reports.py
    crop_reports.py
    market_reports.py

  services/
    data_loader.py
    dataframe_utils.py
    farm_reports.py
    crop_reports.py
    market_reports.py

docs/
  README.md
  API_PLAYBOOK.md
  SYSTEM_BLUEPRINT.md
  DATA_STORY.md
  ENGINEERING_NOTES.md
  assets/
    Project_Architecture.jpeg

notebooks/
  01_comprehensive_eda.ipynb

scripts/
  check_api_endpoints.py
  check_all_endpoints.py
  check_crop_quality_breakdown.py
  check_market_price_comparison.py

Dockerfile
.dockerignore
requirements.txt
README.md
```

---

## Architecture

The backend follows a layered design:

```text
PowerShell / Swagger / Browser
        |
        v
FastAPI Application
        |
        v
Routers
        |
        v
Schemas + Enums
        |
        v
Service Layer
        |
        v
pandas Utility Functions
        |
        v
Data Loader
        |
        v
SQLAlchemy + PyMySQL
        |
        v
Remote MySQL Database
```

Architecture diagram:

![Project Architecture](docs/assets/Project_Architecture.jpeg)

For full system design details, see:

[Open System Blueprint](docs/SYSTEM_BLUEPRINT.md)

---

## Data Sources

The project uses the provided agriculture database.

Main analytical views:

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

Important data decisions:

```text
dim_farm is used for farm_id validation.
dim_crop is used for crop_id, growing season, water requirement, and benchmark yield.
dim_market is used for market district and price tier.
```

For deeper data lineage and transformation notes, see:

[Open Data Story](docs/DATA_STORY.md)

---

## Key Implementation Details

### Yield Efficiency

Actual yield is calculated from harvest records:

```text
actual_avg_yield_ton_per_ha = quantity_harvested_ton / area_planted_ha
```

Benchmark yield comes from:

```text
dim_crop.avg_yield_ton_per_ha
```

Some results may show exactly `100%` efficiency because the sample database contains benchmark-aligned harvest records.

---

### Season Handling

Most endpoints use harvest/calendar season:

```text
Spring, Summer, Autumn, Winter
```

These endpoints use crop growing season:

```text
/farms/loss-analysis
/crops/yield-efficiency
```

Accepted crop growing seasons:

```text
Rabi, Kharif, Zaid, Year-Round
```

---

### Market District Handling

For market price comparison, district is taken from:

```text
dim_market.district
```

not from farm district.

This keeps market location and farm location separate.

---

## Error Handling

The API separates invalid input from valid input with no matching database rows.

### Invalid filter

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=random"
```

Expected:

```text
422 Unprocessable Entity
```

### Valid filter but no matching data

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?district=UnknownDistrict"
```

Expected:

```text
404 Not Found
```

---

## Documentation

Additional documentation is available in the `docs/` folder.

| File | Purpose |
|---|---|
| [API Playbook](docs/API_PLAYBOOK.md) | Endpoint tests, response contracts, and validation behavior |
| [System Blueprint](docs/SYSTEM_BLUEPRINT.md) | Architecture, request lifecycle, Docker runtime, and EDA separation |
| [Data Story](docs/DATA_STORY.md) | Data sources, transformations, and pandas analytics decisions |
| [Engineering Notes](docs/ENGINEERING_NOTES.md) | Design choices, implementation notes, and testing evidence |
| [Docs Index](docs/README.md) | Documentation navigation |

---

## EDA Notebook

The repository includes an exploratory notebook:

```text
notebooks/01_comprehensive_eda.ipynb
```

The notebook contains exploratory analysis and visualization work used to understand the agriculture database before finalizing the API logic.

The notebook is not required for API runtime.

---

## Docker Notes

The Dockerfile uses a multi-stage build.

The final runtime image:

```text
runs as a non-root user
does not copy .env
does not copy local .venv
does not copy notebooks
does not copy .git
```

Database credentials are passed at runtime:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

---

## Current Verification Status

The project has been checked with:

```powershell
python -m compileall app scripts
python scripts\check_api_endpoints.py
docker build -t wegro-agriculture-api .
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Confirmed result:

```text
ALL API SMOKE CHECKS PASSED
Docker build successful
Docker runtime successful
Git working tree clean
```

---

## Repository Notes

This repository intentionally keeps runtime code, documentation, notebook analysis, and Docker setup separated.

The API is designed to be reviewed through:

```text
README.md for running the project
Swagger UI for endpoint inspection
scripts/check_api_endpoints.py for smoke testing
docs/ for deeper technical explanation
notebooks/ for data exploration context
```