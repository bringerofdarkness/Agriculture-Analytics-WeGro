from typing import Any, Optional

import pandas as pd

from app.enums import FarmType, Region, Season, Year
from app.schemas.filters import build_filters_applied
from app.services.data_loader import load_harvest_full
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