# API Playbook

---

## Table of Contents

- [How to Read This Playbook](#how-to-read-this-playbook)
- [Fast Verification Route Map](#fast-verification-route-map)
- [Common Test Setup](#common-test-setup)
- [Report 1 - Farm Performance](#report-1---farm-performance)
  - [Endpoint 1 - Farm Summary](#endpoint-1---farm-summary)
  - [Endpoint 2 - Single Farm Performance](#endpoint-2---single-farm-performance)
  - [Endpoint 3 - Top Farms](#endpoint-3---top-farms)
  - [Endpoint 4 - Loss Analysis](#endpoint-4---loss-analysis)
- [Report 2 - Crop & Market Intelligence](#report-2---crop--market-intelligence)
  - [Endpoint 5 - Crop Yield Efficiency](#endpoint-5---crop-yield-efficiency)
  - [Endpoint 6 - Seasonal Revenue Trend](#endpoint-6---seasonal-revenue-trend)
  - [Endpoint 7 - Market Price Comparison](#endpoint-7---market-price-comparison)
  - [Endpoint 8 - Quality Grade Breakdown](#endpoint-8---quality-grade-breakdown)
- [Validation Behavior](#validation-behavior)
- [One-Command Smoke Test](#one-command-smoke-test)
- [Reviewer Notes](#reviewer-notes)

---

This playbook explains how to review and test the WeGro Agriculture Analytics API.

It is written from the perspective of someone checking the project quickly:

```text
Can the server run?
Are all 8 required routes available?
Do the filters work?
Are the responses shaped correctly?
Do invalid requests fail cleanly?
Does the API return real database-driven results?
```

Base URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 1. How to Read This Playbook

Each endpoint section follows the same review pattern:

```text
Route
Business question
Filters to try
Response contract
PowerShell test command
Reviewer acceptance check
```

This keeps the review focused on actual behavior instead of only listing parameters.

---

## 2. Fast Verification Route Map

```text
Farm Performance
1. /farms/summary
2. /farms/{farm_id}/performance
3. /farms/top
4. /farms/loss-analysis

Crop & Market Intelligence
5. /crops/yield-efficiency
6. /crops/seasonal-trend
7. /markets/price-comparison
8. /crops/quality-breakdown
```

---

## 3. Common Test Setup

In PowerShell:

```powershell
$base = "http://127.0.0.1:8000"
```

Run server locally:

```powershell
uvicorn app.main:app --reload
```

Or run with Docker:

```powershell
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

---

# Report 1 - Farm Performance

---

## Endpoint 1 - Farm Summary

### Route

```text
GET /farms/summary
```

### Business Question

```text
How are farms performing overall in terms of revenue, cost, profit, and loss?
```

### Filters Worth Testing

```text
region
farm_type
year
season
```

Calendar season values:

```text
Spring, Summer, Autumn, Winter
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/farms/summary?region=Dhaka&year=2023" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
total_farms
filters_applied
data
```

Each item inside `data` should contain:

```text
farm_name
region
farm_type
total_revenue_bdt
total_cost_bdt
net_profit_bdt
avg_loss_pct
```

### Acceptance Check

This endpoint is correct if:

```text
The route returns 200 for valid filter combinations.
The response is grouped at farm level.
Revenue, cost, profit, and loss fields are numeric.
No filters return broader farm summary data.
Valid filters with no matching rows return 404.
```

---

## Endpoint 2 - Single Farm Performance

### Route

```text
GET /farms/{farm_id}/performance
```

### Business Question

```text
How did one specific farm perform across crops, years, and market channels?
```

### Filters Worth Testing

```text
year
crop_category
market_type
```

Path rule:

```text
farm_id must be between 1 and 30
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/farms/1/performance?year=2023&crop_category=Cereal" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
farm_id
farm_name
owner
region
filters_applied
performance
```

Each item inside `performance` should contain:

```text
crop_name
year
market_type
quantity_sold_ton
revenue_bdt
net_profit_bdt
quality_grade
```

### Acceptance Check

This endpoint is correct if:

```text
farm_id is validated before analytics are returned.
Invalid farm_id such as 999 returns 422.
The endpoint returns farm metadata and performance rows together.
Filters narrow the performance list without changing the response shape.
```

---

## Endpoint 3 - Top Farms

### Route

```text
GET /farms/top
```

### Business Question

```text
Which farms are the strongest performers by profit, revenue, or yield?
```

### Filters Worth Testing

```text
metric
region
farm_type
year
limit
```

Metric values:

```text
profit, revenue, yield
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/farms/top?metric=profit&limit=5" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
metric
filters_applied
rankings
```

Each item inside `rankings` should contain:

```text
rank
farm_name
region
farm_type
net_profit_bdt
total_revenue_bdt
```

### Acceptance Check

This endpoint is correct if:

```text
/farms/top is used, not /farms/ranking.
Default metric works when metric is omitted.
limit controls the number of returned records.
Invalid metric returns 422.
Rank values are assigned clearly.
```

---

## Endpoint 4 - Loss Analysis

### Route

```text
GET /farms/loss-analysis
```

### Business Question

```text
Where are post-harvest losses happening, and which crop/quality groups are affected?
```

### Filters Worth Testing

```text
region
season
year
quality_grade
crop_category
```

Important:

```text
For this endpoint, season means crop growing season.
```

Accepted season values:

```text
Rabi, Kharif, Zaid, Year-Round
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/farms/loss-analysis?season=Kharif&year=2022&quality_grade=A" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
filters_applied
summary
breakdown
```

`summary` should contain:

```text
total_harvested_ton
total_lost_ton
overall_loss_pct
```

Each item inside `breakdown` should contain:

```text
region
crop_category
quality_grade
total_lost_ton
loss_pct
pesticide_residue
```

### Acceptance Check

This endpoint is correct if:

```text
season accepts Kharif/Rabi/Zaid/Year-Round.
season=Winter should not be accepted here.
The summary totals align with the filtered data.
The breakdown groups losses by meaningful business dimensions.
```

---

# Report 2 - Crop & Market Intelligence

---

## Endpoint 5 - Crop Yield Efficiency

### Route

```text
GET /crops/yield-efficiency
```

### Business Question

```text
Are crops performing above or below their benchmark yield?
```

### Filters Worth Testing

```text
crop_category
season
year
region
water_requirement
```

Important:

```text
For this endpoint, season means crop growing season.
```

Accepted season values:

```text
Rabi, Kharif, Zaid, Year-Round
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/crops/yield-efficiency?crop_category=Vegetable&year=2023&region=Dhaka" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
filters_applied
data
```

Each item inside `data` should contain:

```text
crop_name
crop_category
avg_yield_benchmark_ton_per_ha
actual_avg_yield_ton_per_ha
efficiency_pct
total_area_planted_ha
season
```

### Calculation Logic

Actual yield:

```text
quantity_harvested_ton / area_planted_ha
```

Benchmark yield:

```text
dim_crop.avg_yield_ton_per_ha
```

Efficiency:

```text
actual yield / benchmark yield * 100
```

### Acceptance Check

This endpoint is correct if:

```text
Actual yield is calculated from harvest data.
Benchmark yield comes from crop metadata.
Some rows may show 100% efficiency if the database has benchmark-aligned harvest records.
The API does not fake values to look different from sample examples.
```

---

## Endpoint 6 - Seasonal Revenue Trend

### Route

```text
GET /crops/seasonal-trend
```

### Business Question

```text
How does crop revenue change across seasons, quarters, and years?
```

### Filters Worth Testing

```text
crop_name
crop_category
year
quarter
market_type
```

Correct usage examples:

```text
crop_name=Potato
crop_name=Boro Rice
crop_category=Vegetable
crop_category=Cereal
```

Incorrect usage example:

```text
crop_name=Vegetable
```

Reason:

```text
Vegetable is a crop category, not a crop name.
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/crops/seasonal-trend?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
filters_applied
trend
```

Each item inside `trend` should contain:

```text
crop_name
year
quarter
season
total_quantity_sold_ton
total_revenue_bdt
avg_price_per_ton_bdt
num_harvests
```

### Acceptance Check

This endpoint is correct if:

```text
quarter accepts only 1, 2, 3, or 4.
Revenue and quantity are grouped by crop, year, quarter, and season.
crop_name and crop_category are treated as different concepts.
```

---

## Endpoint 7 - Market Price Comparison

### Route

```text
GET /markets/price-comparison
```

### Business Question

```text
Which market channels, districts, and price tiers give better crop prices?
```

### Filters Worth Testing

```text
market_type
crop_category
year
season
price_tier
district
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/markets/price-comparison?district=Chittagong" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
filters_applied
comparison
```

Each item inside `comparison` should contain:

```text
market_name
market_type
price_tier
district
crop_name
avg_price_per_ton_bdt
total_quantity_sold_ton
total_revenue_bdt
```

### Important Data Rule

```text
district must come from dim_market, not farm district.
```

### Acceptance Check

This endpoint is correct if:

```text
Market district reflects market metadata.
district=Chittagong returns Chittagong market rows when available.
price_tier and market_type filters work together.
Valid district strings with no matching rows return 404.
```

---

## Endpoint 8 - Quality Grade Breakdown

### Route

```text
GET /crops/quality-breakdown
```

### Business Question

```text
How are crop quality grades and pesticide residue levels distributed?
```

### Filters Worth Testing

```text
crop_id
crop_category
year
region
market_type
pesticide_residue
```

### PowerShell Check

```powershell
Invoke-RestMethod "$base/crops/quality-breakdown?crop_category=Vegetable&year=2023" | ConvertTo-Json -Depth 10
```

### Response Contract

A valid response should contain:

```text
filters_applied
total_records
grade_distribution
pesticide_residue_breakdown
```

`grade_distribution` must include:

```text
A
B
C
D
```

Each grade should contain:

```text
count
pct
avg_revenue_bdt
```

`pesticide_residue_breakdown` must include:

```text
None
Trace
Low
High
```

Each residue level should contain:

```text
count
pct
```

### Acceptance Check

This endpoint is correct if:

```text
All grades are returned even when count is zero.
All residue levels are returned even when count is zero.
crop_id filtering works through crop metadata.
The response title in Swagger is Quality Grade Breakdown.
```

---

# Validation Behavior

The API separates invalid input from valid input with no data.

---

## Invalid Input

Example:

```powershell
Invoke-RestMethod "$base/farms/top?metric=random"
```

Expected:

```text
422 Unprocessable Entity
```

Why:

```text
metric is enum-controlled.
random is not an accepted value.
```

---

## No Matching Data

Example:

```powershell
Invoke-RestMethod "$base/markets/price-comparison?district=UnknownDistrict"
```

Expected:

```text
404 Not Found
```

Why:

```text
district is a valid string filter, but no database row matches it.
```

---

# One-Command Smoke Test

Run:

```powershell
python scripts\check_api_endpoints.py
```

Expected final output:

```text
ALL API SMOKE CHECKS PASSED
```

This script verifies:

```text
all 8 success cases
invalid farm ID validation
invalid metric validation
invalid quarter validation
invalid pesticide residue validation
404 no-data behavior
```

---

# Reviewer Notes

A reviewer should focus on these signs of correctness:

```text
1. Routes match the required endpoint paths.
2. Filters narrow the result instead of changing the response contract.
3. Enum-controlled filters return 422 for invalid values.
4. Valid filters with no matching database rows return 404.
5. pandas calculations are database-driven.
6. Output values may differ from static PRD examples because real database data is used.
7. Docker and local runtime both serve the same API.
```

This API playbook is intended to make endpoint verification fast, transparent, and repeatable.