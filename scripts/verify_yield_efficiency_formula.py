import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from app.services.data_loader import load_harvest_full, load_dim_crop

pd.set_option("display.max_columns", 200)
pd.set_option("display.width", 220)

harvest_df = load_harvest_full()
crop_df = load_dim_crop()

merged_df = harvest_df.merge(
    crop_df[
        [
            "crop_name",
            "crop_category",
            "growing_season",
            "avg_yield_ton_per_ha",
        ]
    ],
    on=["crop_name", "crop_category"],
    how="inner",
    suffixes=("_harvest", "_crop"),
)

merged_df["actual_yield_ton_per_ha"] = (
    merged_df["quantity_harvested_ton"] / merged_df["area_planted_ha"]
)

merged_df["yield_difference"] = (
    merged_df["actual_yield_ton_per_ha"] - merged_df["avg_yield_ton_per_ha"]
).round(6)

print("\n=== Yield comparison summary ===")
print("Total matched harvest rows:", len(merged_df))
print("Rows where actual yield equals benchmark:", (merged_df["yield_difference"] == 0).sum())
print("Rows where actual yield differs from benchmark:", (merged_df["yield_difference"] != 0).sum())

print("\n=== Yield difference values ===")
print(merged_df["yield_difference"].value_counts().sort_index().to_string())

print("\n=== Rows where actual yield differs from benchmark ===")
different_df = merged_df[merged_df["yield_difference"] != 0].copy()

print(
    different_df[
        [
            "crop_name",
            "crop_category",
            "region",
            "year",
            "season",
            "growing_season_crop",
            "quantity_harvested_ton",
            "area_planted_ha",
            "actual_yield_ton_per_ha",
            "avg_yield_ton_per_ha",
            "yield_difference",
        ]
    ]
    .sort_values(["year", "region", "crop_category", "crop_name"])
    .to_string(index=False)
)
