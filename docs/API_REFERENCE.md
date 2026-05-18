# WeGro Agriculture Analytics API — API Reference

This document provides endpoint-by-endpoint API documentation for the **WeGro Agriculture Analytics API**.

The API contains 8 required endpoints across two reports:

```text
Report 1: Farm Performance Report
Report 2: Crop & Market Intelligence Report
```

Base URL for local development:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Endpoint Summary

| # | Method | Endpoint | Report |
|---|---|---|---|
| 1 | GET | `/farms/summary` | Farm Performance |
| 2 | GET | `/farms/{farm_id}/performance` | Farm Performance |
| 3 | GET | `/farms/top` | Farm Performance |
| 4 | GET | `/farms/loss-analysis` | Farm Performance |
| 5 | GET | `/crops/yield-efficiency` | Crop & Market Intelligence |
| 6 | GET | `/crops/seasonal-trend` | Crop & Market Intelligence |
| 7 | GET | `/markets/price-comparison` | Crop & Market Intelligence |
| 8 | GET | `/crops/quality-breakdown` | Crop & Market Intelligence |

---

# Report 1: Farm Performance Report

## 1. Farm Summary

```text
GET /farms/summary
```

### Purpose

Returns a summary of farms with total revenue, total cost, net profit, and average post-harvest loss percentage.

If no filters are passed, the endpoint returns farm summary data across all available records.

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `region` | enum | No | Filter by farm region |
| `farm_type` | enum | No | Filter by farm type |
| `year` | enum/integer | No | Filter by year |
| `season` | enum | No | Filter by harvest/calendar season |

### Accepted Values

```text
region: Dhaka, Chittagong, Sylhet, Rajshahi, Khulna, Rangpur, Barisal, Mymensingh
farm_type: Small, Medium, Large, Commercial
year: 2022, 2023, 2024
season: Spring, Summer, Autumn, Winter
```

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/summary?region=Dhaka&year=2023" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "total_farms": 2,
  "filters_applied": {
    "region": "Dhaka",
    "year": 2023
  },
  "data": [
    {
      "farm_name": "Example Farm",
      "region": "Dhaka",
      "farm_type": "Large",
      "total_revenue_bdt": 4250000,
      "total_cost_bdt": 980000,
      "net_profit_bdt": 3270000,
      "avg_loss_pct": 4.2
    }
  ]
}
```

---

## 2. Single Farm Performance

```text
GET /farms/{farm_id}/performance
```

### Purpose

Returns detailed performance for one specific farm. It shows crop-wise revenue, profit, quantity sold, year, market channel, and quality grade.

The `farm_id` is validated against the farm dimension table.

### Path Parameter

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `farm_id` | integer | Yes | Farm ID from `dim_farm`; accepted range: 1 to 30 |

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `year` | enum/integer | No | Filter by year |
| `crop_category` | enum | No | Filter by crop category |
| `market_type` | enum | No | Filter by market type |

### Accepted Values

```text
year: 2022, 2023, 2024
crop_category: Cereal, Vegetable, Fruit, Pulse, Oilseed, Cash Crop, Spice
market_type: Local, Wholesale, Export, Retail, Government Procurement
```

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/1/performance?year=2023&crop_category=Cereal" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "farm_id": 1,
  "farm_name": "Example Farm",
  "owner": "Example Owner",
  "region": "Dhaka",
  "filters_applied": {
    "year": 2023,
    "crop_category": "Cereal"
  },
  "performance": [
    {
      "crop_name": "Boro Rice",
      "year": 2023,
      "market_type": "Wholesale",
      "quantity_sold_ton": 60.0,
      "revenue_bdt": 1560000,
      "net_profit_bdt": 1180000,
      "quality_grade": "A"
    }
  ]
}
```

---

## 3. Top Farms Ranking

```text
GET /farms/top
```

### Purpose

Returns the top farms ranked by a selected metric.

Supported ranking metrics:

```text
profit
revenue
yield
```

Default metric:

```text
profit
```

Default limit:

```text
10
```

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `metric` | enum | No | Ranking metric |
| `region` | enum | No | Filter by region |
| `farm_type` | enum | No | Filter by farm type |
| `year` | enum/integer | No | Filter by year |
| `limit` | integer | No | Number of farms to return |

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=profit&region=Rajshahi&limit=5" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "metric": "profit",
  "filters_applied": {
    "region": "Rajshahi",
    "limit": 5
  },
  "rankings": [
    {
      "rank": 1,
      "farm_name": "Example Farm",
      "region": "Rajshahi",
      "farm_type": "Commercial",
      "net_profit_bdt": 8900000,
      "total_revenue_bdt": 11200000
    }
  ]
}
```

---

## 4. Loss Analysis

```text
GET /farms/loss-analysis
```

### Purpose

Shows post-harvest loss analysis by region, crop category, quality grade, and pesticide residue level.

This endpoint uses **crop growing season** values, not calendar season values.

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `region` | enum | No | Filter by region |
| `season` | enum | No | Filter by crop growing season |
| `year` | enum/integer | No | Filter by year |
| `quality_grade` | enum | No | Filter by quality grade |
| `crop_category` | enum | No | Filter by crop category |

### Accepted Season Values

```text
Rabi, Kharif, Zaid, Year-Round
```

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "filters_applied": {
    "season": "Kharif",
    "year": 2022,
    "quality_grade": "A"
  },
  "summary": {
    "total_harvested_ton": 1240.5,
    "total_lost_ton": 98.2,
    "overall_loss_pct": 7.9
  },
  "breakdown": [
    {
      "region": "Chittagong",
      "crop_category": "Cereal",
      "quality_grade": "A",
      "total_lost_ton": 42.5,
      "loss_pct": 9.1,
      "pesticide_residue": "Trace"
    }
  ]
}
```

---

# Report 2: Crop & Market Intelligence Report

## 5. Crop Yield Efficiency

```text
GET /crops/yield-efficiency
```

### Purpose

Compares actual crop yield per hectare against benchmark crop yield.

Actual yield is calculated from harvest records:

```text
actual_avg_yield_ton_per_ha = quantity_harvested_ton / area_planted_ha
```

Benchmark yield comes from:

```text
dim_crop.avg_yield_ton_per_ha
```

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `crop_category` | enum | No | Filter by crop category |
| `season` | enum | No | Filter by crop growing season |
| `year` | enum/integer | No | Filter by year |
| `region` | enum | No | Filter by region |
| `water_requirement` | enum | No | Filter by crop water requirement |

### Accepted Season Values

```text
Rabi, Kharif, Zaid, Year-Round
```

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/yield-efficiency?crop_category=Vegetable&year=2023&region=Dhaka" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "filters_applied": {
    "crop_category": "Vegetable",
    "year": 2023,
    "region": "Dhaka"
  },
  "data": [
    {
      "crop_name": "Potato",
      "crop_category": "Vegetable",
      "avg_yield_benchmark_ton_per_ha": 22.0,
      "actual_avg_yield_ton_per_ha": 21.5,
      "efficiency_pct": 97.73,
      "total_area_planted_ha": 10.0,
      "season": "Rabi"
    }
  ]
}
```

---

## 6. Seasonal Revenue Trend

```text
GET /crops/seasonal-trend
```

### Purpose

Shows how revenue and quantity sold change across seasons, years, and quarters for each crop.

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `crop_name` | string | No | Filter by crop name |
| `crop_category` | enum | No | Filter by crop category |
| `year` | enum/integer | No | Filter by year |
| `quarter` | enum/integer | No | Filter by quarter |
| `market_type` | enum | No | Filter by market type |

### Important Note

`crop_name` expects actual crop names such as:

```text
Potato
Tomato
Boro Rice
Aman Rice
Maize
```

Do not pass category values such as `Vegetable` into `crop_name`.  
Use `crop_category=Vegetable` instead.

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/seasonal-trend?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "filters_applied": {
    "crop_category": "Vegetable",
    "year": 2023
  },
  "trend": [
    {
      "crop_name": "Potato",
      "year": 2023,
      "quarter": 1,
      "season": "Winter",
      "total_quantity_sold_ton": 392.0,
      "total_revenue_bdt": 8624000,
      "avg_price_per_ton_bdt": 22000,
      "num_harvests": 4
    }
  ]
}
```

---

## 7. Market Price Comparison

```text
GET /markets/price-comparison
```

### Purpose

Compares crop selling prices across market names, market types, districts, and price tiers.

This endpoint uses `dim_market` to ensure district and price tier come from market metadata.

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `market_type` | enum | No | Filter by market type |
| `crop_category` | enum | No | Filter by crop category |
| `year` | enum/integer | No | Filter by year |
| `season` | enum | No | Filter by harvest/calendar season |
| `price_tier` | enum | No | Filter by price tier |
| `district` | string | No | Filter by market district |

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?crop_category=Cereal&year=2023&market_type=Export" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "filters_applied": {
    "crop_category": "Cereal",
    "year": 2023,
    "market_type": "Export"
  },
  "comparison": [
    {
      "market_name": "Chittagong Port Market",
      "market_type": "Export",
      "price_tier": "Premium",
      "district": "Chittagong",
      "crop_name": "Aman Rice",
      "avg_price_per_ton_bdt": 48000,
      "total_quantity_sold_ton": 87.0,
      "total_revenue_bdt": 4176000
    }
  ]
}
```

---

## 8. Quality Grade Breakdown

```text
GET /crops/quality-breakdown
```

### Purpose

Shows crop quality grade distribution and pesticide residue breakdown.

The endpoint returns all quality grades:

```text
A, B, C, D
```

And all pesticide residue levels:

```text
None, Trace, Low, High
```

Even if a category has zero matching records, it is still included with count `0`.

### Query Filters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `crop_id` | integer/string | No | Filter by crop ID |
| `crop_category` | enum | No | Filter by crop category |
| `year` | enum/integer | No | Filter by year |
| `region` | enum | No | Filter by region |
| `market_type` | enum | No | Filter by market type |
| `pesticide_residue` | enum | No | Filter by pesticide residue level |

### Example Request

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/crops/quality-breakdown?crop_category=Fruit&year=2023&region=Rajshahi" | ConvertTo-Json -Depth 10
```

### Response Shape

```json
{
  "filters_applied": {
    "crop_category": "Fruit",
    "year": 2023,
    "region": "Rajshahi"
  },
  "total_records": 8,
  "grade_distribution": {
    "A": {
      "count": 5,
      "pct": 62.5,
      "avg_revenue_bdt": 1840000
    },
    "B": {
      "count": 2,
      "pct": 25.0,
      "avg_revenue_bdt": 920000
    },
    "C": {
      "count": 1,
      "pct": 12.5,
      "avg_revenue_bdt": 380000
    },
    "D": {
      "count": 0,
      "pct": 0.0,
      "avg_revenue_bdt": 0
    }
  },
  "pesticide_residue_breakdown": {
    "None": {
      "count": 6,
      "pct": 75.0
    },
    "Trace": {
      "count": 2,
      "pct": 25.0
    },
    "Low": {
      "count": 0,
      "pct": 0.0
    },
    "High": {
      "count": 0,
      "pct": 0.0
    }
  }
}
```

---

# Error Handling

The API uses structured error handling.

## Invalid Filter Value

Invalid enum/path values return:

```text
422 Unprocessable Entity
```

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/farms/top?metric=random"
```

Expected:

```text
422
```

## Valid Filter but No Matching Rows

Valid filters that produce no matching database records return:

```text
404 Not Found
```

Example:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/markets/price-comparison?district=UnknownDistrict"
```

Expected:

```text
404
```

---

# Smoke Test Coverage

The project includes a smoke test script:

```text
scripts/check_api_endpoints.py
```

Run:

```powershell
python scripts\check_api_endpoints.py
```

Expected output:

```text
ALL API SMOKE CHECKS PASSED
```

The smoke test checks:

```text
8 successful endpoint cases
Invalid farm ID validation
Invalid ranking metric validation
Invalid quarter validation
Invalid pesticide residue validation
404 no-data cases
```

---

# Notes

The API responses are generated from the real assessment database.  
Some values may differ from static PRD examples because the PRD examples are illustrative.

The important criteria are:

```text
Correct endpoint path
Correct filter behavior
Correct aggregation logic
Correct response shape
Correct HTTP status codes
```