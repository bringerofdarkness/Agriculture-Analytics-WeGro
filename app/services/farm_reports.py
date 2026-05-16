from typing import Any, Optional

import pandas as pd

from app.enums import CropCategory, FarmType, MarketType, Region, Season, Year
from app.schemas.filters import build_filters_applied
from app.services.data_loader import load_dim_farm, load_harvest_full
from app.services.dataframe_utils import (
    apply_optional_filters,
    dataframe_to_records,
    ensure_dataframe_not_empty,
    round_numeric_columns,
    validate_required_columns,
)


FARM_SUMMARY_REQUIRED_COLUMNS: set[str] = {
    "farm_name",
    "region",
    "farm_type",
    "year",
    "season",
    "revenue_bdt",
    "input_cost_bdt",
    "net_profit_bdt",
    "quantity_harvested_ton",
    "quantity_lost_ton",
}

DIM_FARM_REQUIRED_COLUMNS: set[str] = {
    "farm_id",
    "farm_name",
    "owner_name",
    "region",
}

SINGLE_FARM_PERFORMANCE_REQUIRED_COLUMNS: set[str] = {
    "farm_name",
    "crop_name",
    "crop_category",
    "year",
    "market_type",
    "quantity_sold_ton",
    "revenue_bdt",
    "net_profit_bdt",
    "quality_grade",
}


def _add_loss_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add row-level post-harvest loss percentage.

    Formula:
        quantity_lost_ton / quantity_harvested_ton * 100

    Zero-harvest rows are safely handled as 0.0 loss percentage.
    """
    result = df.copy()

    result["loss_pct"] = 0.0

    valid_harvest_mask = result["quantity_harvested_ton"].gt(0)

    result.loc[valid_harvest_mask, "loss_pct"] = (
        result.loc[valid_harvest_mask, "quantity_lost_ton"]
        / result.loc[valid_harvest_mask, "quantity_harvested_ton"]
        * 100
    )

    return result


def get_farm_summary(
    *,
    region: Optional[Region] = None,
    farm_type: Optional[FarmType] = None,
    year: Optional[Year] = None,
    season: Optional[Season] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /farms/summary.

    Supported PRD filters:
        - region
        - farm_type
        - year
        - season
    """
    df = load_harvest_full()

    validate_required_columns(df, FARM_SUMMARY_REQUIRED_COLUMNS)

    filtered_df = apply_optional_filters(
        df,
        {
            "region": region,
            "farm_type": farm_type,
            "year": year,
            "season": season,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No farm summary data found for the requested filters.",
    )

    filtered_df = _add_loss_percentage(filtered_df)

    summary_df = (
        filtered_df.groupby(["farm_name", "region", "farm_type"], as_index=False)
        .agg(
            total_revenue_bdt=("revenue_bdt", "sum"),
            total_cost_bdt=("input_cost_bdt", "sum"),
            net_profit_bdt=("net_profit_bdt", "sum"),
            avg_loss_pct=("loss_pct", "mean"),
        )
        .sort_values(
            by=["net_profit_bdt", "total_revenue_bdt", "farm_name"],
            ascending=[False, False, True],
        )
        .reset_index(drop=True)
    )

    summary_df = round_numeric_columns(summary_df, decimals=2)

    return {
        "total_farms": int(summary_df["farm_name"].nunique()),
        "filters_applied": build_filters_applied(
            {
                "region": region,
                "farm_type": farm_type,
                "year": year,
                "season": season,
            }
        ),
        "data": dataframe_to_records(summary_df),
    }


def get_single_farm_performance(
    *,
    farm_id: int,
    year: Optional[Year] = None,
    crop_category: Optional[CropCategory] = None,
    market_type: Optional[MarketType] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /farms/{farm_id}/performance.

    Supported PRD filters:
        - year
        - crop_category
        - market_type
    """
    farms_df = load_dim_farm()

    validate_required_columns(farms_df, DIM_FARM_REQUIRED_COLUMNS)

    farm_df = farms_df.loc[farms_df["farm_id"].eq(farm_id)].copy()

    ensure_dataframe_not_empty(
        farm_df,
        f"No farm found for farm_id={farm_id}.",
    )

    farm_record = farm_df.iloc[0]

    farm_name = str(farm_record["farm_name"])
    owner_name = str(farm_record["owner_name"])
    region_name = str(farm_record["region"])

    harvest_df = load_harvest_full()

    validate_required_columns(harvest_df, SINGLE_FARM_PERFORMANCE_REQUIRED_COLUMNS)

    farm_harvest_df = harvest_df.loc[harvest_df["farm_name"].eq(farm_name)].copy()

    filtered_df = apply_optional_filters(
        farm_harvest_df,
        {
            "year": year,
            "crop_category": crop_category,
            "market_type": market_type,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No performance data found for the requested farm and filters.",
    )

    performance_df = (
        filtered_df.groupby(
            ["crop_name", "year", "market_type", "quality_grade"],
            as_index=False,
        )
        .agg(
            quantity_sold_ton=("quantity_sold_ton", "sum"),
            revenue_bdt=("revenue_bdt", "sum"),
            net_profit_bdt=("net_profit_bdt", "sum"),
        )
        .sort_values(
            by=["year", "crop_name", "market_type", "quality_grade"],
            ascending=[True, True, True, True],
        )
        .reset_index(drop=True)
    )

    performance_df = performance_df[
        [
            "crop_name",
            "year",
            "market_type",
            "quantity_sold_ton",
            "revenue_bdt",
            "net_profit_bdt",
            "quality_grade",
        ]
    ]

    performance_df = round_numeric_columns(performance_df, decimals=2)

    return {
        "farm_id": int(farm_id),
        "farm_name": farm_name,
        "owner": owner_name,
        "region": region_name,
        "filters_applied": build_filters_applied(
            {
                "year": year,
                "crop_category": crop_category,
                "market_type": market_type,
            }
        ),
        "performance": dataframe_to_records(performance_df),
    }