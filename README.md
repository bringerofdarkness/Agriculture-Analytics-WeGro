# WeGro Agriculture Analytics API

FastAPI + pandas based analytics API for the WeGro agriculture assessment.

This project reads from a remote MySQL agriculture database, transforms the data with pandas, and serves farm, crop, market, loss, yield, and quality insights through 8 API endpoints.

---

## What This Project Does

The API answers practical agriculture analytics questions:

- Which farms are generating the best revenue and profit?
- How does one farm perform across crops and market channels?
- Which farms rank highest by profit, revenue, or yield?
- Where are post-harvest losses happening?
- Which crops are performing above or below benchmark yield?
- How does crop revenue change by season and quarter?
- Which markets provide better crop prices?
- How are quality grades and pesticide residue levels distributed?

The backend is read-only. It does not modify the database.

---

## Run the Project Locally

### 1. Clone

```powershell
git clone https://github.com/bringerofdarkness/Agriculture-Analytics-WeGro.git
cd Agriculture-Analytics-WeGro
```

### 2. Create `.env`

Create a `.env` file in the project root:

```env
HOST=your_mysql_host
PORT=3306
USER=your_mysql_username
PASSWORD=your_mysql_password
DATABASE=agriculture_db
```

The `.env` file is not committed to GitHub.

### 3. Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install Requirements

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start FastAPI

```powershell
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

The project supports three Docker-based workflows:

```text
1. Quick PowerShell runner
2. Docker Compose
3. Manual docker build/run
```

Before running Docker, make sure a `.env` file exists in the project root.

A safe template is provided:

```text
.env.example
```

Create your local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Then update `.env` with the actual database credentials.

---

### Option 1: Run with PowerShell Helper

For Windows PowerShell, the easiest way to run the Dockerized API is:

```powershell
.\run-docker.ps1
```

This script will:

```text
check if .env exists
build the Docker image
remove any old container with the same name
start the API container
wait for /health to pass
print the Swagger and health URLs
```

Expected output includes:

```text
Container is healthy.
Swagger UI: http://127.0.0.1:8000/docs
Health URL: http://127.0.0.1:8000/health
```

If PowerShell blocks script execution, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-docker.ps1
```

To stop the container:

```powershell
docker stop wegro-agriculture-api
docker rm wegro-agriculture-api
```

---

### Option 2: Run with Docker Compose

Build and start the API:

```powershell
docker compose up --build
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Check health:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/health" | ConvertTo-Json -Depth 5
```

Expected health response:

```json
{
  "status": "healthy",
  "service": "wegro-agriculture-api",
  "version": "1.0.0"
}
```

Stop and remove the Compose container/network:

```powershell
docker compose down
```

---

### Option 3: Manual Docker Build and Run

Build the image:

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

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

### Docker Health Check

The API includes a lightweight health endpoint:

```text
GET /health
```

The Docker image also includes a container-level `HEALTHCHECK` that calls this endpoint.

Check container health:

```powershell
docker ps
```

Or inspect the health status directly:

```powershell
docker inspect --format='{{json .State.Health.Status}}' wegro-agriculture-api
```

Expected result:

```text
"healthy"
```

---

### Docker Notes

The Docker setup is designed to keep the runtime image clean.

The Docker image does not copy:

```text
.env
.venv
.git
notebooks
cache files
local development artifacts
```

The container runs the FastAPI application as a non-root user.

Database credentials are passed at runtime through:

```powershell
--env-file .env
```

If port `8000` is already in use, either stop the running process/container or map a different host port:

```powershell
docker run --rm --env-file .env -p 8001:8000 wegro-agriculture-api
```

Then open:

```text
http://127.0.0.1:8001/docs
```

---

## API Route Map

Base URL:

```text
http://127.0.0.1:8000
```

### Farm Performance

| No. | Endpoint | Purpose |
|---|---|---|
| 1 | `GET /farms/summary` | Farm-level revenue, cost, profit, and loss summary |
| 2 | `GET /farms/{farm_id}/performance` | Detailed performance for a single farm |
| 3 | `GET /farms/top` | Top farms by profit, revenue, or yield |
| 4 | `GET /farms/loss-analysis` | Post-harvest loss analysis |

### Crop & Market Intelligence

| No. | Endpoint | Purpose |
|---|---|---|
| 5 | `GET /crops/yield-efficiency` | Actual crop yield compared with benchmark yield |
| 6 | `GET /crops/seasonal-trend` | Crop revenue and quantity trend by season and quarter |
| 7 | `GET /markets/price-comparison` | Market price comparison by crop, market, district, and tier |
| 8 | `GET /crops/quality-breakdown` | Quality grade and pesticide residue distribution |

For detailed endpoint tests and response contracts:

[docs/API_PLAYBOOK.md](docs/API_PLAYBOOK.md)

---

## Example PowerShell Requests

```powershell
$base = "http://127.0.0.1:8000"
```

### Farm Summary

```powershell
Invoke-RestMethod "$base/farms/summary?region=Dhaka&year=2023" | ConvertTo-Json -Depth 10
```

### Single Farm Performance

```powershell
Invoke-RestMethod "$base/farms/1/performance?year=2023&crop_category=Cereal" | ConvertTo-Json -Depth 10
```

### Top Farms

```powershell
Invoke-RestMethod "$base/farms/top?metric=profit&limit=5" | ConvertTo-Json -Depth 10
```

### Loss Analysis

```powershell
Invoke-RestMethod "$base/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A" | ConvertTo-Json -Depth 10
```

### Yield Efficiency

```powershell
Invoke-RestMethod "$base/crops/yield-efficiency?crop_category=Vegetable&year=2023&region=Dhaka" | ConvertTo-Json -Depth 10
```

### Seasonal Revenue Trend

```powershell
Invoke-RestMethod "$base/crops/seasonal-trend?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

### Market Price Comparison

```powershell
Invoke-RestMethod "$base/markets/price-comparison?district=Chittagong" | ConvertTo-Json -Depth 10
```

### Quality Grade Breakdown

```powershell
Invoke-RestMethod "$base/crops/quality-breakdown?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

---

## Technology Used

| Area | Stack |
|---|---|
| API | FastAPI |
| Server | Uvicorn |
| Data Processing | pandas |
| Database | MySQL |
| Database Connection | SQLAlchemy + PyMySQL |
| Validation | Pydantic |
| Runtime | Python 3.11 |
| Containerization | Docker |

---

## Code Layout

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

scripts/
  check_api_endpoints.py
  check_all_endpoints.py
  check_crop_quality_breakdown.py
  check_market_price_comparison.py

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
```

---

## How the Backend Is Organized

The project follows a layered flow:

```text
PowerShell / Swagger / Browser
        |
        v
FastAPI app
        |
        v
Routers
        |
        v
Schemas and Enums
        |
        v
Service functions
        |
        v
pandas utilities
        |
        v
Data loader
        |
        v
SQLAlchemy + PyMySQL
        |
        v
Remote MySQL database
```

Architecture image:

![Project Architecture](docs/assets/Project_Architecture.jpeg)

More details:

[docs/SYSTEM_BLUEPRINT.md](docs/SYSTEM_BLUEPRINT.md)

---

## Data Sources

The API uses the provided agriculture database.

Main views:

```text
vw_harvest_full
vw_revenue_by_crop_year
vw_farm_profitability
```

Dimension tables used when needed:

```text
dim_farm
dim_crop
dim_market
```

Why dimension tables are used:

- `dim_farm` validates `farm_id`
- `dim_crop` provides `crop_id`, growing season, water requirement, and benchmark yield
- `dim_market` provides market district and price tier

More data notes:

[docs/DATA_STORY.md](docs/DATA_STORY.md)

---

## Important Implementation Notes

### Yield Efficiency

Actual yield is calculated from harvest data:

```text
actual_yield = quantity_harvested_ton / area_planted_ha
```

Benchmark yield comes from:

```text
dim_crop.avg_yield_ton_per_ha
```

Some rows can show exactly `100%` efficiency because the database contains benchmark-aligned harvest records.

---

### Season Handling

Most endpoints use calendar or harvest season:

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

### Market District

For market price comparison, district comes from:

```text
dim_market.district
```

not from farm district.

This keeps farm location and market location separate.

---

## Error Handling

The API separates invalid requests from valid requests that return no data.

### Invalid filter value

Example:

```powershell
Invoke-RestMethod "$base/farms/top?metric=random"
```

Expected:

```text
422 Unprocessable Entity
```

### Valid filter but no matching row

Example:

```powershell
Invoke-RestMethod "$base/markets/price-comparison?district=UnknownDistrict"
```

Expected:

```text
404 Not Found
```

---

## EDA Notebook

The repository includes:

```text
notebooks/01_comprehensive_eda.ipynb
```

The notebook contains exploratory analysis and visualizations used to understand the database before finalizing the API logic.

The notebook is not required to run the FastAPI app.

---

## Documentation

| File | Purpose |
|---|---|
| [API Playbook](docs/API_PLAYBOOK.md) | Endpoint testing flow, examples, response contracts, and validation notes |
| [System Blueprint](docs/SYSTEM_BLUEPRINT.md) | Request lifecycle, architecture layers, Docker runtime, and system boundaries |
| [Data Story](docs/DATA_STORY.md) | Data lineage, pandas transformation logic, and source table usage |
| [Engineering Notes](docs/ENGINEERING_NOTES.md) | Design decisions, fixes, testing evidence, and implementation notes |
| [Docs Index](docs/README.md) | Documentation navigation |

---

## Docker Notes

The final Docker image does not copy:

```text
.env
.venv
.git
notebooks
cache files
```

Database credentials are passed at runtime:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

---

## Current Verification

The project has been checked with:

```powershell
python -m compileall app scripts
python scripts\check_api_endpoints.py
docker build -t wegro-agriculture-api .
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Confirmed:

```text
All smoke tests passed
Docker build passed
Docker runtime passed
```

---

## Notes

This repository keeps the API code, documentation, Docker setup, and EDA notebook separate.

The API is intended to be reviewed through:

```text
README.md
Swagger UI
PowerShell endpoint checks
scripts/check_api_endpoints.py
docs/
notebooks/
```