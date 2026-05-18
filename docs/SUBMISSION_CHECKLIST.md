# Submission Readiness Checklist

This checklist is the final review guide for the WeGro Agriculture Analytics API before submitting the public GitHub repository.

The goal is simple:

```text
The evaluator should be able to clone the repo, configure the environment, run the API, open Swagger, test all endpoints, and verify the project without confusion.
```

---

## 1. Repository Readiness

| Check | Status |
|---|---|
| Public GitHub repository is available | ☐ |
| Root `README.md` exists | ☐ |
| `requirements.txt` exists | ☐ |
| `Dockerfile` exists | ☐ |
| `.dockerignore` exists | ☐ |
| Source code is inside `app/` | ☐ |
| Test scripts are inside `scripts/` | ☐ |
| EDA notebook is inside `notebooks/` | ☐ |
| Supporting documentation is inside `docs/` | ☐ |
| Architecture image is inside `docs/assets/` | ☐ |
| Git working tree is clean | ☐ |

Final Git check:

```powershell
git status
```

Expected:

```text
nothing to commit, working tree clean
```

---

## 2. Secret and Credential Safety

Before submission, confirm that no real database credentials are committed.

| Check | Status |
|---|---|
| `.env` is not committed | ☐ |
| Real database host is not exposed in notebook output | ☐ |
| Real database password is not visible anywhere | ☐ |
| API code does not hardcode credentials | ☐ |
| Docker image does not copy `.env` | ☐ |
| `.dockerignore` excludes `.env`, `.venv`, `.git`, cache files | ☐ |

Required local `.env` format:

```env
HOST=your_mysql_host
PORT=3306
USER=your_mysql_username
PASSWORD=your_mysql_password
DATABASE=agriculture_db
```

Security rule:

```text
The evaluator should create their own .env file locally.
The repository should not contain real credentials.
```

---

## 3. Local Python Runtime Check

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Compile check:

```powershell
python -m compileall app scripts
```

Expected:

```text
No Python syntax errors
```

Checklist:

| Check | Status |
|---|---|
| Virtual environment activates successfully | ☐ |
| Dependencies install from `requirements.txt` | ☐ |
| `python -m compileall app scripts` passes | ☐ |

---

## 4. FastAPI Server Check

Run locally:

```powershell
uvicorn app.main:app --reload
```

Expected:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Checklist:

| Check | Status |
|---|---|
| FastAPI app starts successfully | ☐ |
| Swagger UI opens | ☐ |
| OpenAPI JSON opens at `/openapi.json` | ☐ |
| All 8 endpoints are visible in Swagger | ☐ |

---

## 5. Required Endpoint Checklist

The API must expose all 8 assessment endpoints.

| # | Endpoint | Status |
|---|---|---|
| 1 | `GET /farms/summary` | ☐ |
| 2 | `GET /farms/{farm_id}/performance` | ☐ |
| 3 | `GET /farms/top` | ☐ |
| 4 | `GET /farms/loss-analysis` | ☐ |
| 5 | `GET /crops/yield-efficiency` | ☐ |
| 6 | `GET /crops/seasonal-trend` | ☐ |
| 7 | `GET /markets/price-comparison` | ☐ |
| 8 | `GET /crops/quality-breakdown` | ☐ |

Important naming checks:

```text
Use /farms/top, not /farms/ranking.
Use /markets/price-comparison for market analysis.
Use /crops/quality-breakdown with summary title "Quality Grade Breakdown".
```

---

## 6. Manual Endpoint Smoke Commands

Use these commands from a second PowerShell window while the API is running.

### Farm Summary

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/summary" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains total_farms, filters_applied, data
```

---

### Single Farm Performance

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/1/performance" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains farm_id, farm_name, owner, region, filters_applied, performance
```

---

### Top Farms

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=profit&limit=5" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains metric, filters_applied, rankings
```

---

### Loss Analysis

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains filters_applied, summary, breakdown
```

---

### Crop Yield Efficiency

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/yield-efficiency?year=2022" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains filters_applied and data
```

---

### Seasonal Revenue Trend

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/seasonal-trend?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains filters_applied and trend
```

---

### Market Price Comparison

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?district=Chittagong" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains filters_applied and comparison
Market district should come from dim_market
```

---

### Quality Grade Breakdown

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/quality-breakdown?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

Expected:

```text
200 OK
Response contains filters_applied, total_records, grade_distribution, pesticide_residue_breakdown
```

---

## 7. Automated Smoke Test

Run:

```powershell
python scripts\check_api_endpoints.py
```

Expected final line:

```text
ALL API SMOKE CHECKS PASSED
```

Checklist:

| Check | Status |
|---|---|
| All 8 success cases pass | ☐ |
| Invalid farm ID returns 422 | ☐ |
| Invalid ranking metric returns 422 | ☐ |
| Invalid quarter returns 422 | ☐ |
| Invalid pesticide residue returns 422 | ☐ |
| No-data market case returns 404 | ☐ |
| No-data crop quality case returns 404 | ☐ |

---

## 8. Error Handling Review

The API should distinguish between invalid input and no matching data.

### Invalid input

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=random"
```

Expected:

```text
422 Unprocessable Entity
```

Reason:

```text
metric is enum-controlled and random is not accepted.
```

---

### Valid input but no matching rows

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?district=UnknownDistrict"
```

Expected:

```text
404 Not Found
```

Reason:

```text
district is a valid string filter, but no database row matches that district.
```

Checklist:

| Check | Status |
|---|---|
| Invalid filters do not produce raw stack traces | ☐ |
| No-data cases return clear messages | ☐ |
| 422 and 404 are used for different situations | ☐ |

---

## 9. Docker Build and Runtime Check

Build image:

```powershell
docker build -t wegro-agriculture-api .
```

Expected:

```text
Build completed successfully
```

Run container:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

Expected:

```text
Application startup complete.
Uvicorn running on http://0.0.0.0:8000
```

From another PowerShell window:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/summary" | ConvertTo-Json -Depth 10
```

Checklist:

| Check | Status |
|---|---|
| Docker image builds | ☐ |
| Docker container starts | ☐ |
| API is reachable from host machine | ☐ |
| Docker run uses `.env` at runtime | ☐ |
| Docker image does not include notebook or local virtual environment | ☐ |

---

## 10. Documentation Review

| File | Purpose | Status |
|---|---|---|
| `README.md` | Main setup and usage guide | ☐ |
| `docs/README.md` | Documentation index | ☐ |
| `docs/ARCHITECTURE.md` | System design and request lifecycle | ☐ |
| `docs/API_REFERENCE.md` | Endpoint reference | ☐ |
| `docs/DATA_GUIDE.md` | Data story and analytics lineage | ☐ |
| `docs/PROJECT_REFERENCE.md` | Technical decisions and reviewer notes | ☐ |
| `docs/SUBMISSION_CHECKLIST.md` | Final readiness checklist | ☐ |

Documentation should be:

```text
accurate
not copied from another repository
consistent with actual code
clear enough for a recruiter to follow
```

---

## 11. Notebook Review

Notebook:

```text
notebooks/01_comprehensive_eda.ipynb
```

Checklist:

| Check | Status |
|---|---|
| Notebook opens successfully | ☐ |
| Visualizations are visible | ☐ |
| Notebook supports project understanding | ☐ |
| No password or secret is visible | ☐ |
| Notebook is not required for API runtime | ☐ |

---

## 12. Final Evaluation Mapping

| Evaluation Area | Evidence in This Project | Status |
|---|---|---|
| Database connection | SQLAlchemy + PyMySQL + `.env` configuration | ☐ |
| pandas processing | Service layer transformations and aggregations | ☐ |
| FastAPI endpoints | All 8 endpoints implemented and tested | ☐ |
| Code quality | Layered architecture and reusable utilities | ☐ |
| Error handling | 422 and 404 cases tested | ☐ |
| Docker bonus | Multi-stage Dockerfile and runtime verification | ☐ |

---

## 13. Final Command Sequence

Run this before submission:

```powershell
python -m compileall app scripts
python scripts\check_api_endpoints.py
docker build -t wegro-agriculture-api .
git status
```

Expected result:

```text
compileall passes
ALL API SMOKE CHECKS PASSED
Docker build passes
working tree clean
```

Optional Docker runtime check:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

---

## 14. Submission Confidence Statement

The project is ready to submit when the following are true:

```text
All endpoint tests pass.
Docker build and run are verified.
README explains local and Docker setup.
Documentation is original and project-specific.
No credentials are committed.
GitHub repository is public.
Git working tree is clean.
```

At that point, the repository is ready for recruiter review.