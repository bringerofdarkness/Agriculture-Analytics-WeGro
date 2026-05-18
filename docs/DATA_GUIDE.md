# WeGro Agriculture Analytics API — Data Guide

This document explains the data sources, database views, dimension tables, pandas transformations, and EDA notebook used in the **WeGro Agriculture Analytics API**.

The API is built on top of the provided agriculture database for the WeGro Technologies Limited Associate Data Scientist Technical Assessment.

---

## 1. Database Overview

The project uses the provided remote MySQL database:

```text
agriculture_db
```

The database follows a Star Schema-based structure. The API consumes the provided analytical views and selected dimension tables to generate report outputs.

The backend does not create or modify database records.  
It only reads data, processes it with pandas, and returns analytics through FastAPI endpoints.

---

## 2. Main Analytical Views Used

The PRD recommended using the pre-built views because they simplify report generation.

The project mainly uses:

```text
vw_harvest_full
vw_revenue_by_crop_year
vw_farm_profitability
```

---

## 3. vw_harvest_full

`vw_harvest_full` is the primary data source for most endpoints.

It contains joined harvest, farm, crop, market, date, input, revenue, profit, quality, and loss information.

Common columns used from this view include:

```text
harvest_id
farm_name
owner_name
region
farm_district
farm_type
total_area_ha
crop_name
crop_category
growing_season
full_date
month_name
quarter
year
season
supply_name
supply_type
is_organic
market_name
market_type
price_tier
area_planted_ha
quantity_harvested_ton
quantity_sold_ton
quantity_lost_ton
price_per_ton_bdt
revenue_bdt
input_cost_bdt
net_profit_bdt
quality_grade
moisture_pct
pesticide_residue
```

Used by:

```text
/farms/summary
/farms/{farm_id}/performance
/farms/loss-analysis
/crops/yield-efficiency
/crops/seasonal-trend
/markets/price-comparison
/crops/quality-breakdown
```

---

## 4. vw_farm_profitability

`vw_farm_profitability` is used for farm profitability and ranking analytics.

It supports:

```text
/farms/top
```

Typical analytics from this view include:

```text
farm-level revenue
farm-level input cost
net profit
ranking by profit
ranking by revenue
ranking by yield
```

---

## 5. vw_revenue_by_crop_year

`vw_revenue_by_crop_year` is available as a recommended PRD view for crop-year revenue analysis.

The project keeps data loading support for this view through the data loader so that the analytics layer can be extended if more crop-year revenue endpoints are required in the future.

---

## 6. Dimension Tables Used

Although the PRD recommends the views, some endpoints need extra metadata from dimension tables.

The project uses:

```text
dim_farm
dim_crop
dim_market
```

---

## 7. dim_farm

Used for farm metadata and farm ID validation.

Important columns:

```text
farm_id
farm_name
owner_name
region
farm_type
```

Used by:

```text
/farms/{farm_id}/performance
```

Why it is needed:

```text
vw_harvest_full contains farm_name but not farm_id.
The endpoint path requires farm_id.
Therefore, dim_farm is used to validate farm_id and map it to farm_name.
```

---

## 8. dim_crop

Used for crop metadata, benchmark yield, crop ID filtering, growing season, and water requirement.

Important columns:

```text
crop_id
crop_name
crop_category
growing_season
avg_yield_ton_per_ha
water_requirement
```

Used by:

```text
/farms/loss-analysis
/crops/yield-efficiency
/crops/quality-breakdown
```

Why it is needed:

```text
Crop yield benchmark is stored in dim_crop.
Crop ID filtering requires dim_crop because vw_harvest_full does not directly contain crop_id.
Crop growing season values come from dim_crop.
```

---

## 9. dim_market

Used for market metadata, market district, and market price tier.

Important columns:

```text
market_name
market_type
district
price_tier
```

Used by:

```text
/markets/price-comparison
```

Why it is needed:

```text
Market district should come from dim_market.
It should not be confused with farm district from farm-related records.
```

---

## 10. Data Loading Layer

Data loading is handled in:

```text
app/services/data_loader.py
```

This layer reads allowlisted database views and dimension tables.

Data is loaded through:

```text
pandas.read_sql()
SQLAlchemy Engine
PyMySQL Driver
```

Correct flow:

```text
Service function
→ data_loader.py
→ database.py
→ SQLAlchemy Engine
→ PyMySQL Driver
→ Remote MySQL Database
→ pandas DataFrame
```

The data loader prevents unsafe arbitrary reads by keeping approved sources allowlisted.

---

## 11. pandas Processing Approach

The API uses pandas after reading data from MySQL.

Common pandas operations include:

```text
filtering
merge
groupby
aggregation
sorting
rounding
percentage calculation
record serialization
```

The shared helper file is:

```text
app/services/dataframe_utils.py
```

Common utility functions:

```text
apply_optional_filters()
validate_required_columns()
ensure_dataframe_not_empty()
round_numeric_columns()
dataframe_to_records()
```

This keeps analytics service files cleaner and avoids repeated pandas code.

---

## 12. Endpoint-Level Data Usage

### Farm Summary

Endpoint:

```text
GET /farms/summary
```

Main source:

```text
vw_harvest_full
```

Main operations:

```text
filter by region, farm_type, year, season
group by farm_name, region, farm_type
sum revenue_bdt
sum input_cost_bdt
sum net_profit_bdt
calculate average loss percentage
```

---

### Single Farm Performance

Endpoint:

```text
GET /farms/{farm_id}/performance
```

Main sources:

```text
dim_farm
vw_harvest_full
```

Main operations:

```text
validate farm_id using dim_farm
map farm_id to farm_name
filter harvest records for that farm
optional filters: year, crop_category, market_type
group crop performance records
return farm metadata and performance rows
```

---

### Top Farms Ranking

Endpoint:

```text
GET /farms/top
```

Main source:

```text
vw_farm_profitability
```

Main operations:

```text
filter by region, farm_type, year
rank by selected metric
apply limit
return ranked farms
```

Supported metrics:

```text
profit
revenue
yield
```

---

### Loss Analysis

Endpoint:

```text
GET /farms/loss-analysis
```

Main sources:

```text
vw_harvest_full
dim_crop
```

Main operations:

```text
join crop metadata where required
filter by region, year, growing season, quality_grade, crop_category
sum harvested quantity
sum lost quantity
calculate overall loss percentage
group loss by region, crop_category, quality_grade, pesticide_residue
```

Important season note:

```text
This endpoint uses crop growing season:
Rabi, Kharif, Zaid, Year-Round
```

---

### Crop Yield Efficiency

Endpoint:

```text
GET /crops/yield-efficiency
```

Main sources:

```text
vw_harvest_full
dim_crop
```

Main operations:

```text
filter harvest data by crop_category, year, region
filter crop benchmark data by crop_category, growing season, water_requirement
join harvest records with crop benchmark data
calculate actual yield
compare actual yield with benchmark yield
calculate efficiency percentage
```

Formula:

```text
actual_avg_yield_ton_per_ha = quantity_harvested_ton / area_planted_ha
```

Benchmark:

```text
dim_crop.avg_yield_ton_per_ha
```

Efficiency:

```text
efficiency_pct = actual_avg_yield_ton_per_ha / avg_yield_benchmark_ton_per_ha * 100
```

Important note:

```text
Some actual yields may equal benchmark yields because the provided sample database contains benchmark-aligned harvest records.
```

---

### Seasonal Revenue Trend

Endpoint:

```text
GET /crops/seasonal-trend
```

Main source:

```text
vw_harvest_full
```

Main operations:

```text
filter by crop_name, crop_category, year, quarter, market_type
group by crop_name, year, quarter, season
sum quantity_sold_ton
sum revenue_bdt
calculate average price per ton
count harvest records
```

Important note:

```text
crop_name expects actual crop names such as Potato, Tomato, Boro Rice, Aman Rice, or Maize.
crop_category should be used for values like Vegetable or Cereal.
```

---

### Market Price Comparison

Endpoint:

```text
GET /markets/price-comparison
```

Main sources:

```text
vw_harvest_full
dim_market
```

Main operations:

```text
join market metadata
filter by market_type, crop_category, year, season, price_tier, district
group by market_name, market_type, price_tier, district, crop_name
calculate average selling price
sum quantity sold
sum revenue
```

Important note:

```text
district comes from dim_market, not farm district.
```

---

### Quality Grade Breakdown

Endpoint:

```text
GET /crops/quality-breakdown
```

Main sources:

```text
vw_harvest_full
dim_crop
```

Main operations:

```text
join crop metadata for crop_id support
filter by crop_id, crop_category, year, region, market_type, pesticide_residue
count total records
calculate quality grade distribution
calculate pesticide residue distribution
calculate average revenue by grade
```

Returned quality grades:

```text
A, B, C, D
```

Returned pesticide residue levels:

```text
None, Trace, Low, High
```

Zero-count categories are still included for complete response shape.

---

## 13. EDA Notebook

The repository includes:

```text
notebooks/01_comprehensive_eda.ipynb
```

Purpose:

```text
Explore the agriculture database
Understand available columns
Check distribution of farms, crops, markets, and seasons
Create visualizations
Support business insight generation before API implementation
```

The notebook supports the data science side of the project.

It is not part of the production API runtime.

---

## 14. Docker and Data Files

The Docker image includes:

```text
app/
requirements.txt
installed dependencies
runtime Python environment
```

The Docker image excludes:

```text
notebooks/
.env
.git
local .venv
cache files
```

Database credentials are passed at runtime through:

```bash
docker run --rm --env-file .env -p 8000:8000 wegro-agriculture-api
```

---

## 15. Data Quality and Validation Notes

The API includes safeguards for:

```text
missing required columns
empty filtered DataFrames
invalid enum filter values
valid filters that produce no rows
```

Behavior:

```text
Invalid enum/path filter → 422
Valid filter but no matching rows → 404
```

This keeps responses predictable and avoids raw errors being returned to API users.

---

## 16. Summary

The data layer is designed to be:

```text
read-only
pandas-friendly
modular
safe through allowlisted sources
aligned with the PRD views
clear for recruiter evaluation
```

The API uses the database as the source of truth and avoids hardcoded output values.