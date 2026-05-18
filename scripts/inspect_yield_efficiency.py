import pandas as pd

from app.services.data_loader import load_harvest_full, load_dim_crop

pd.set_option("display.max_columns", 200)
pd.set_option("display.width", 200)

harvest_df = load_harvest_full()
crop_df = load_dim_crop()

print("\n=== vw_harvest_full columns ===")
print(list(harvest_df.columns))

print("\n=== dim_crop columns ===")
print(list(crop_df.columns))

# Match the same Swagger test you showed
filtered = harvest_df[
    (harvest_df["crop_category"] == "Cereal")
    & (harvest_df["year"] == 2022)
    & (harvest_df["region"] == "Rangpur")
].copy()

print("\n=== Filtered harvest rows: Cereal, 2022, Rangpur ===")
print("Rows:", len(filtered))

possible_harvest_cols = [
    "crop_name",
    "crop_category",
    "region",
    "year",
    "season",
    "quantity_harvested_ton",
    "total_harvested_ton",
    "quantity_sold_ton",
    "area_planted_ha",
    "total_area_planted_ha",
    "yield_ton_per_ha",
    "actual_yield_ton_per_ha",
    "avg_yield_benchmark_ton_per_ha",
]

existing_harvest_cols = [col for col in possible_harvest_cols if col in filtered.columns]

print("\n=== Relevant harvest sample ===")
print(filtered[existing_harvest_cols].head(20).to_string(index=False))

possible_crop_cols = [
    "crop_id",
    "crop_name",
    "crop_category",
    "growing_season",
    "water_requirement",
    "avg_yield_benchmark_ton_per_ha",
]

existing_crop_cols = [col for col in possible_crop_cols if col in crop_df.columns]

print("\n=== dim_crop benchmark data for Cereal ===")
print(
    crop_df[crop_df["crop_category"] == "Cereal"][existing_crop_cols]
    .sort_values("crop_name")
    .to_string(index=False)
)

print("\n=== Columns containing 'yield' in harvest view ===")
print([col for col in harvest_df.columns if "yield" in col.lower()])

print("\n=== Columns containing 'area' in harvest view ===")
print([col for col in harvest_df.columns if "area" in col.lower()])

print("\n=== Columns containing 'harvest' in harvest view ===")
print([col for col in harvest_df.columns if "harvest" in col.lower()])
