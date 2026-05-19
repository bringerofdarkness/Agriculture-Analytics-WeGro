# Project Reference - WeGro Agriculture Analytics API

---

## Table of Contents

- [Project Reference - WeGro Agriculture Analytics API](#project-reference---wegro-agriculture-analytics-api)
  - [Table of Contents](#table-of-contents)
  - [1. Project Identity](#1-project-identity)
  - [2. What This Project Solves](#2-what-this-project-solves)
  - [3. Assessment Requirement Mapping](#3-assessment-requirement-mapping)
  - [4. Final Endpoint Inventory](#4-final-endpoint-inventory)
  - [5. Implementation Style](#5-implementation-style)
  - [6. Main Code Areas](#6-main-code-areas)
    - [API entry point](#api-entry-point)
    - [Routers](#routers)
    - [Schemas](#schemas)
    - [Enums](#enums)
    - [Services](#services)
    - [Data access](#data-access)
  - [7. Engineering Decisions](#7-engineering-decisions)
    - [Decision 1: Keep routers thin](#decision-1-keep-routers-thin)
    - [Decision 2: Use enums for filter validation](#decision-2-use-enums-for-filter-validation)
    - [Decision 3: Use pandas after loading database views](#decision-3-use-pandas-after-loading-database-views)
    - [Decision 4: Use dimension tables only where required](#decision-4-use-dimension-tables-only-where-required)
    - [Decision 5: Keep helper functions stateless](#decision-5-keep-helper-functions-stateless)
    - [Decision 6: Do not fake PRD example values](#decision-6-do-not-fake-prd-example-values)
  - [8. Important Data Interpretation Notes](#8-important-data-interpretation-notes)
    - [Season has two meanings](#season-has-two-meanings)
    - [Market district must come from dim\_market](#market-district-must-come-from-dim_market)
    - [crop\_name and crop\_category are different](#crop_name-and-crop_category-are-different)
  - [9. Endpoint Implementation Notes](#9-endpoint-implementation-notes)
    - [/farms/summary](#farmssummary)
    - [/farms/{farm\_id}/performance](#farmsfarm_idperformance)
    - [/farms/top](#farmstop)
    - [/farms/loss-analysis](#farmsloss-analysis)
    - [/crops/yield-efficiency](#cropsyield-efficiency)
    - [/crops/seasonal-trend](#cropsseasonal-trend)
    - [/markets/price-comparison](#marketsprice-comparison)
    - [/crops/quality-breakdown](#cropsquality-breakdown)
  - [10. Testing Evidence](#10-testing-evidence)
  - [11. Docker Verification](#11-docker-verification)
  - [12. Documentation Strategy](#12-documentation-strategy)
  - [13. Recruiter Review Path](#13-recruiter-review-path)
  - [14. Known Safe Assumptions](#14-known-safe-assumptions)
  - [15. Final Confidence Summary](#15-final-confidence-summary)
  
---

This document is the internal technical reference for the WeGro Agriculture Analytics API.

It explains what was built, why key implementation decisions were made, how the project satisfies the assessment requirements, and how the final system should be reviewed by an evaluator.

This is not a duplicate of the root README.  
The root README is for running the project.  
This document is for understanding the project deeply.

---

## 1. Project Identity

Project name:

```text
WeGro Agriculture Analytics API
```

Repository purpose:

```text
Associate Data Scientist Technical Assessment
WeGro Technologies Limited
```

Core idea:

```text
Transform agriculture database records into clean, filterable analytics endpoints using FastAPI and pandas.
```

The project behaves like a small data product:

```text
database -> pandas analytics -> validated API responses -> recruiter-testable endpoints
```

---

## 2. What This Project Solves

The provided agriculture database contains farm, crop, harvest, market, revenue, profit, loss, quality, and pesticide residue information.

The API converts that data into decision-ready insights such as:

```text
Which farms are profitable?
Which crops are underperforming against benchmark yield?
Which regions suffer higher post-harvest losses?
Which markets provide better prices?
How are crop quality grades distributed?
How does revenue change by season and quarter?
```

Instead of only exposing raw database rows, the backend returns structured summaries and business-focused analytics.

---

## 3. Assessment Requirement Mapping

The assessment expects a FastAPI backend connected to MySQL, using pandas for processing, and exposing 8 required endpoints.

This project maps to those requirements as follows:

| Requirement Area | Project Implementation |
|---|---|
| MySQL connection | SQLAlchemy engine with PyMySQL driver |
| Secure configuration | Database credentials loaded from `.env` |
| pandas processing | Filtering, merging, grouping, aggregation, and metric calculation |
| FastAPI endpoints | All 8 required endpoints implemented |
| Validation | Enum-based query/path validation |
| Response shape | Pydantic response schemas |
| Error handling | 422 for invalid filters, 404 for valid filters with no rows |
| Docker support | Multi-stage Dockerfile with non-root runtime user |
| Documentation | Root README plus supporting docs folder |
| EDA | Notebook included for data exploration and visualization |

---

## 4. Final Endpoint Inventory

The API implements all required endpoints:

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

These endpoints are grouped into two reports:

```text
Farm Performance Report
Crop & Market Intelligence Report
```

---

## 5. Implementation Style

The project follows a layered backend style.

```text
Routers only handle HTTP concerns.
Schemas and enums handle validation.
Services handle analytics.
DataFrame utilities handle reusable pandas operations.
Data loader handles controlled database reads.
Database module handles SQLAlchemy connectivity.
```

This keeps the code easier to review.

A recruiter can inspect one endpoint and quickly understand the pattern used across the rest of the project.

---

## 6. Main Code Areas

### API entry point

```text
app/main.py
```

Used for:

```text
FastAPI app creation
router registration
Swagger/OpenAPI configuration
global exception handling
```

### Routers

```text
app/routers/farms.py
app/routers/crops.py
app/routers/markets.py
app/routers/crop_quality.py
```

Used for:

```text
endpoint path declaration
query/path parameter declaration
response model attachment
service function calls
```

### Schemas

```text
app/schemas/farm_reports.py
app/schemas/crop_reports.py
app/schemas/market_reports.py
app/schemas/filters.py
```

Used for:

```text
response models
filter aliases
clean response validation
Swagger parameter documentation
```

### Enums

```text
app/enums/filters.py
```

Used for accepted filter values such as:

```text
region
farm_type
crop_category
season
market_type
price_tier
quality_grade
pesticide_residue
year
quarter
metric
```

### Services

```text
app/services/farm_reports.py
app/services/crop_reports.py
app/services/market_reports.py
```

Used for:

```text
business logic
pandas transformations
metric calculations
response assembly
```

### Data access

```text
app/config.py
app/database.py
app/services/data_loader.py
```

Used for:

```text
environment configuration
SQLAlchemy engine creation
allowlisted database reads
pandas DataFrame loading
```

---

## 7. Engineering Decisions

### Decision 1: Keep routers thin

Routers should not contain heavy pandas logic.

Reason:

```text
Thin routers make the API layer easier to read and keep analytics testable inside service modules.
```

---

### Decision 2: Use enums for filter validation

Invalid filters should fail early.

Example:

```text
/farms/top?metric=random
```

Expected:

```text
422 Unprocessable Entity
```

Reason:

```text
FastAPI enum validation gives clean Swagger dropdowns and avoids manually checking every invalid string.
```

---

### Decision 3: Use pandas after loading database views

The assessment specifically expects pandas processing.

Reason:

```text
pandas is ideal for grouping, aggregation, filtering, merging, and business metric calculation.
```

---

### Decision 4: Use dimension tables only where required

The project mainly uses analytical views, but dimension tables are used when endpoint requirements require metadata.

Examples:

```text
dim_farm -> farm_id validation
dim_crop -> crop_id, benchmark yield, growing season
dim_market -> market district and price tier
```

Reason:

```text
This avoids unnecessary joins while still satisfying endpoint requirements correctly.
```

---

### Decision 5: Keep helper functions stateless

Reusable pandas helpers are stored in:

```text
app/services/dataframe_utils.py
```

Reason:

```text
Stateless helpers are easier to reuse, test, and reason about.
```

---

### Decision 6: Do not fake PRD example values

The PRD examples are static examples.  
The API must return values from the real database.

Example:

```text
Crop yield efficiency can show 100% when actual yield equals benchmark yield.
```

Reason:

```text
The correct behavior is to calculate honestly from database values, not force outputs to look like a sample screenshot.
```

---

## 8. Important Data Interpretation Notes

### Season has two meanings

Some endpoints use harvest/calendar season:

```text
Spring
Summer
Autumn
Winter
```

Some endpoints use crop growing season:

```text
Rabi
Kharif
Zaid
Year-Round
```

Growing season is used for:

```text
/farms/loss-analysis
/crops/yield-efficiency
```

Reason:

```text
Those endpoints analyze crop-growing behavior, not only calendar harvest timing.
```

---

### Market district must come from dim_market

The market price endpoint should use market district, not farm district.

Correct interpretation:

```text
dim_market.district
```

Reason:

```text
A farm location and a market location are different business concepts.
```

---

### crop_name and crop_category are different

Correct examples:

```text
crop_name=Potato
crop_name=Boro Rice
crop_category=Vegetable
crop_category=Cereal
```

Incorrect usage:

```text
crop_name=Vegetable
```

Reason:

```text
Vegetable is a category, not an individual crop name.
```

---

## 9. Endpoint Implementation Notes

### /farms/summary

Focus:

```text
farm-level summary
```

Calculates:

```text
total revenue
total cost
net profit
average loss percentage
```

---

### /farms/{farm_id}/performance

Focus:

```text
single farm detailed performance
```

Key logic:

```text
validate farm_id using dim_farm
map farm_id to farm_name
filter harvest data by farm_name
return crop-year-market details
```

---

### /farms/top

Focus:

```text
ranking farms
```

Supports:

```text
profit
revenue
yield
```

---

### /farms/loss-analysis

Focus:

```text
post-harvest loss
```

Key logic:

```text
use crop growing season
calculate total harvested quantity
calculate total lost quantity
calculate loss percentage
group by region, crop_category, quality_grade, pesticide_residue
```

---

### /crops/yield-efficiency

Focus:

```text
actual yield vs benchmark yield
```

Formula:

```text
actual_avg_yield_ton_per_ha = quantity_harvested_ton / area_planted_ha
```

Benchmark source:

```text
dim_crop.avg_yield_ton_per_ha
```

---

### /crops/seasonal-trend

Focus:

```text
crop revenue trend over season, quarter, and year
```

Calculates:

```text
total quantity sold
total revenue
average price per ton
number of harvests
```

---

### /markets/price-comparison

Focus:

```text
market-level price comparison
```

Key correction:

```text
district comes from dim_market, not farm district.
```

---

### /crops/quality-breakdown

Focus:

```text
quality grade and pesticide residue distribution
```

Response includes all:

```text
quality grades: A, B, C, D
residue levels: None, Trace, Low, High
```

Zero-count categories are preserved.

---

## 10. Testing Evidence

The project has been tested with:

```text
python -m compileall app scripts
python scripts/check_api_endpoints.py
docker build -t wegro-agriculture-api .
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
PowerShell Invoke-RestMethod endpoint checks
Swagger UI checks
```

Latest confirmed smoke test result:

```text
ALL API SMOKE CHECKS PASSED
```

Smoke test coverage includes:

```text
8 successful endpoint responses
invalid farm ID validation
invalid ranking metric validation
invalid quarter validation
invalid pesticide residue validation
404 no-data scenarios
```

---

## 11. Docker Verification

Docker build command:

```powershell
docker build -t wegro-agriculture-api .
```

Docker run command:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Confirmed runtime status:

```text
Application startup complete.
Uvicorn running on http://0.0.0.0:8000
```

Docker design:

```text
multi-stage build
non-root runtime user
no local .env copied into image
no local .venv copied into image
no notebooks copied into image
```

---

## 12. Documentation Strategy

The documentation is split intentionally.

```text
README.md
```

Main user-facing run guide.

```text
docs/README.md
```

Documentation index.

```text
docs/SYSTEM_BLUEPRINT.md
```

System architecture and request lifecycle.

```text
docs/API_PLAYBOOK.md
```

Endpoint-by-endpoint API guide.

```text
docs/DATA_STORY.md
```

Data story, lineage, and pandas transformation notes.

```text
docs/ENGINEERING_NOTES.md
```

Engineering decisions and reviewer notes.

```text
```


This keeps the root README readable while still giving evaluators deeper technical context.

---

## 13. Recruiter Review Path

A reviewer can evaluate the project in this order:

```text
1. Read root README.md.
2. Create .env file.
3. Install requirements.
4. Run uvicorn app.main:app --reload.
5. Open /docs.
6. Test the 8 endpoints.
7. Run python scripts/check_api_endpoints.py.
8. Build and run Docker image.
9. Review docs/SYSTEM_BLUEPRINT.md and docs/API_PLAYBOOK.md.
10. Check notebooks/01_comprehensive_eda.ipynb for EDA context.
```

This path is designed to make project review simple and low-friction.

---

## 14. Known Safe Assumptions

The project assumes:

```text
The provided MySQL database is reachable.
The .env file contains valid credentials.
The database contains the PRD-required views and dimension tables.
The evaluator runs the API locally on port 8000 or maps Docker port 8000.
```

The project does not assume:

```text
database credentials are public
PRD example values exactly match real database values
notebooks are required for API runtime
Docker image should contain .env
```

---

## 15. Final Confidence Summary

The final project is ready because:

```text
all 8 required endpoints are implemented
all success smoke tests pass
expected validation errors return 422
expected no-data cases return 404
Docker build passes
Docker run passes
Git working tree is clean
documentation is organized
EDA notebook is included
credentials are not committed
```

The project is suitable for submission as a public GitHub repository.
