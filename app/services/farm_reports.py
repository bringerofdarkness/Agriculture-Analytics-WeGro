from typing import Any, Optional
import pandas as pd

from app.enums import (
    CropCategory,
    FarmType,
    GrowingSeason,
    MarketType,
    QualityGrade,
    RankingMetric,
    Region,
    Season,
    Year,
)
from app.schemas.filters import build_filters_applied
from app.services.data_loader import (
    load_dim_crop,
    load_dim_farm,
    load_harvest_full,
)
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

TOP_FARMS_REQUIRED_COLUMNS: set[str] = {
    "farm_name",
    "region",
    "farm_type",
    "year",
    "revenue_bdt",
    "net_profit_bdt",
    "quantity_harvested_ton",
    "area_planted_ha",
}

LOSS_ANALYSIS_HARVEST_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "year",
    "region",
    "quality_grade",
    "quantity_harvested_ton",
    "quantity_lost_ton",
    "pesticide_residue",
}

LOSS_ANALYSIS_CROP_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "growing_season",
}


def _add_loss_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add row-level post-harvest loss percentage safely.
    """
    result = df.copy()
    result["loss_pct"] = 0.0

    valid_harvest_mask = result["quantity_harvested_ton"].gt(0)
    if valid_harvest_mask.any():
        result.loc[valid_harvest_mask, "loss_pct"] = (
            result.loc[valid_harvest_mask, "quantity_lost_ton"].fillna(0.0)
            / result.loc[valid_harvest_mask, "quantity_harvested_ton"]
            * 100
        )
    return result


def _add_yield_per_hectare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add yield per hectare safely for internal ranking calculations.
    """
    result = df.copy()
    result["yield_ton_per_ha"] = 0.0

    valid_area_mask = result["area_planted_ha"].gt(0)
    if valid_area_mask.any():
        result.loc[valid_area_mask, "yield_ton_per_ha"] = (
            result.loc[valid_area_mask, "quantity_harvested_ton"].fillna(0.0)
            / result.loc[valid_area_mask, "area_planted_ha"]
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
    )
    
    
    summary_df["avg_loss_pct"] = summary_df["avg_loss_pct"].fillna(0.0)

    summary_df = (
        summary_df.sort_values(
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


def get_top_farms_ranking(
    *,
    metric: RankingMetric = RankingMetric.PROFIT,
    region: Optional[Region] = None,
    farm_type: Optional[FarmType] = None,
    year: Optional[Year] = None,
    limit: int = 10,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /farms/top.
    """
    df = load_harvest_full()
    validate_required_columns(df, TOP_FARMS_REQUIRED_COLUMNS)

    filtered_df = apply_optional_filters(
        df,
        {
            "region": region,
            "farm_type": farm_type,
            "year": year,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No farm ranking data found for the requested filters.",
    )

    filtered_df = _add_yield_per_hectare(filtered_df)

    ranking_df = (
        filtered_df.groupby(["farm_name", "region", "farm_type"], as_index=False)
        .agg(
            net_profit_bdt=("net_profit_bdt", "sum"),
            total_revenue_bdt=("revenue_bdt", "sum"),
            yield_ton_per_ha=("yield_ton_per_ha", "mean"),
        )
    )
    
    ranking_df["yield_ton_per_ha"] = ranking_df["yield_ton_per_ha"].fillna(0.0)

    metric_sort_column = {
        RankingMetric.PROFIT: "net_profit_bdt",
        RankingMetric.REVENUE: "total_revenue_bdt",
        RankingMetric.YIELD: "yield_ton_per_ha",
    }[metric]

    ranking_df = (
        ranking_df.sort_values(
            by=[metric_sort_column, "farm_name"],
            ascending=[False, True],
        )
        .head(limit)
        .reset_index(drop=True)
    )

    ranking_df.insert(0, "rank", ranking_df.index + 1)

    ranking_df = ranking_df[
        [
            "rank",
            "farm_name",
            "region",
            "farm_type",
            "net_profit_bdt",
            "total_revenue_bdt",
        ]
    ]

    ranking_df = round_numeric_columns(ranking_df, decimals=2)

    return {
        "metric": metric.value,
        "filters_applied": build_filters_applied(
            {
                "region": region,
                "farm_type": farm_type,
                "year": year,
                "limit": limit,
            }
        ),
        "rankings": dataframe_to_records(ranking_df),
    }


def get_farm_loss_analysis(
    *,
    region: Optional[Region] = None,
    year: Optional[Year] = None,
    season: Optional[GrowingSeason] = None,
    quality_grade: Optional[QualityGrade] = None,
    crop_category: Optional[CropCategory] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /farms/loss-analysis.
    """
    harvest_df = load_harvest_full()
    crop_df = load_dim_crop()

    validate_required_columns(harvest_df, LOSS_ANALYSIS_HARVEST_REQUIRED_COLUMNS)
    validate_required_columns(crop_df, LOSS_ANALYSIS_CROP_REQUIRED_COLUMNS)

    crop_lookup_df = (
        crop_df[["crop_name", "crop_category", "growing_season"]]
        .drop_duplicates()
        .rename(columns={"growing_season": "crop_growing_season"})
    )

    df = harvest_df.merge(
        crop_lookup_df,
        on=["crop_name", "crop_category"],
        how="left",
    )

    if df["crop_growing_season"].isna().any():
        raise ValueError("Operational Error: Missing mapping relational crop data from dim_crop.")

    filtered_df = apply_optional_filters(
        df,
        {
            "region": region,
            "crop_growing_season": season,
            "year": year,
            "quality_grade": quality_grade,
            "crop_category": crop_category,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No loss analysis data found for the requested filters.",
    )

    total_harvested_ton = float(filtered_df["quantity_harvested_ton"].sum())
    total_lost_ton = float(filtered_df["quantity_lost_ton"].sum())

    overall_loss_pct = (
        total_lost_ton / total_harvested_ton * 100
        if total_harvested_ton > 0
        else 0.0
    )

    breakdown_df = (
        filtered_df.groupby(
            ["region", "crop_category", "quality_grade", "pesticide_residue"],
            as_index=False,
        )
        .agg(
            total_harvested_ton=("quantity_harvested_ton", "sum"),
            total_lost_ton=("quantity_lost_ton", "sum"),
        )
    )

    breakdown_df["loss_pct"] = 0.0
    valid_harvest_mask = breakdown_df["total_harvested_ton"].gt(0)
    
    if valid_harvest_mask.any():
        breakdown_df.loc[valid_harvest_mask, "loss_pct"] = (
            breakdown_df.loc[valid_harvest_mask, "total_lost_ton"]
            / breakdown_df.loc[valid_harvest_mask, "total_harvested_ton"]
            * 100
        )

    breakdown_df = breakdown_df[
        [
            "region",
            "crop_category",
            "quality_grade",
            "total_lost_ton",
            "loss_pct",
            "pesticide_residue",
        ]
    ]

    breakdown_df = (
        breakdown_df.sort_values(
            by=["loss_pct", "total_lost_ton", "region", "crop_category"],
            ascending=[False, False, True, True],
        )
        .reset_index(drop=True)
    )

    breakdown_df = round_numeric_columns(breakdown_df, decimals=2)

    return {
        "filters_applied": build_filters_applied(
            {
                "region": region,
                "season": season,
                "year": year,
                "quality_grade": quality_grade,
                "crop_category": crop_category,
            }
        ),
        "summary": {
            "total_harvested_ton": round(total_harvested_ton, 2),
            "total_lost_ton": round(total_lost_ton, 2),
            "overall_loss_pct": round(overall_loss_pct, 2),
        },
        "breakdown": dataframe_to_records(breakdown_df),
    }