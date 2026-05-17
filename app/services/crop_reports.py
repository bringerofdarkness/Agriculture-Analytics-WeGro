from typing import Any, Optional

from app.enums import (
    CropCategory,
    MarketType,
    PesticideResidue,
    Quarter,
    Region,
    Season,
    WaterRequirement,
    Year,
)
from app.schemas.filters import build_filters_applied
from app.services.data_loader import load_dim_crop, load_harvest_full
from app.services.dataframe_utils import (
    apply_optional_filters,
    dataframe_to_records,
    ensure_dataframe_not_empty,
    round_numeric_columns,
    validate_required_columns,
)


YIELD_EFFICIENCY_HARVEST_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "year",
    "season",
    "region",
    "area_planted_ha",
    "quantity_harvested_ton",
}

YIELD_EFFICIENCY_CROP_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "growing_season",
    "avg_yield_ton_per_ha",
    "water_requirement",
}

SEASONAL_TREND_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "year",
    "quarter",
    "season",
    "market_type",
    "quantity_sold_ton",
    "revenue_bdt",
    "price_per_ton_bdt",
    "harvest_id",
}

QUALITY_BREAKDOWN_HARVEST_REQUIRED_COLUMNS: set[str] = {
    "crop_name",
    "crop_category",
    "year",
    "region",
    "market_type",
    "pesticide_residue",
    "quality_grade",
    "revenue_bdt",
}

QUALITY_BREAKDOWN_CROP_REQUIRED_COLUMNS: set[str] = {
    "crop_id",
    "crop_name",
    "crop_category",
}

QUALITY_GRADES: tuple[str, ...] = ("A", "B", "C", "D")
PESTICIDE_RESIDUE_LEVELS: tuple[str, ...] = ("None", "Trace", "Low", "High")


def get_crop_yield_efficiency(
    *,
    crop_category: Optional[CropCategory] = None,
    season: Optional[Season] = None,
    year: Optional[Year] = None,
    region: Optional[Region] = None,
    water_requirement: Optional[WaterRequirement] = None,
) -> dict[str, Any]:
    harvest_df = load_harvest_full()
    crop_df = load_dim_crop()

    validate_required_columns(harvest_df, YIELD_EFFICIENCY_HARVEST_REQUIRED_COLUMNS)
    validate_required_columns(crop_df, YIELD_EFFICIENCY_CROP_REQUIRED_COLUMNS)

    filtered_harvest_df = apply_optional_filters(
        harvest_df,
        {
            "crop_category": crop_category,
            "season": season,
            "year": year,
            "region": region,
        },
    )

    filtered_crop_df = apply_optional_filters(
        crop_df,
        {
            "crop_category": crop_category,
            "water_requirement": water_requirement,
        },
    )

    ensure_dataframe_not_empty(
        filtered_harvest_df,
        "No harvest data found for the requested yield efficiency filters.",
    )
    ensure_dataframe_not_empty(
        filtered_crop_df,
        "No crop benchmark data found for the requested yield efficiency filters.",
    )

    benchmark_df = (
        filtered_crop_df[
            [
                "crop_name",
                "crop_category",
                "growing_season",
                "avg_yield_ton_per_ha",
                "water_requirement",
            ]
        ]
        .drop_duplicates()
        .rename(columns={"growing_season": "crop_season"})
    )

    merged_df = filtered_harvest_df.merge(
        benchmark_df,
        on=["crop_name", "crop_category"],
        how="inner",
    )

    ensure_dataframe_not_empty(
        merged_df,
        "No matching crop yield efficiency data found for the requested filters.",
    )

    efficiency_df = (
        merged_df.groupby(["crop_name", "crop_category", "crop_season"], as_index=False)
        .agg(
            avg_yield_benchmark_ton_per_ha=("avg_yield_ton_per_ha", "mean"),
            total_area_planted_ha=("area_planted_ha", "sum"),
            total_quantity_harvested_ton=("quantity_harvested_ton", "sum"),
        )
        .reset_index(drop=True)
    )

    efficiency_df["actual_avg_yield_ton_per_ha"] = 0.0
    valid_area_mask = efficiency_df["total_area_planted_ha"].gt(0)

    efficiency_df.loc[valid_area_mask, "actual_avg_yield_ton_per_ha"] = (
        efficiency_df.loc[valid_area_mask, "total_quantity_harvested_ton"]
        / efficiency_df.loc[valid_area_mask, "total_area_planted_ha"]
    )

    efficiency_df["efficiency_pct"] = 0.0
    valid_benchmark_mask = efficiency_df["avg_yield_benchmark_ton_per_ha"].gt(0)

    efficiency_df.loc[valid_benchmark_mask, "efficiency_pct"] = (
        efficiency_df.loc[valid_benchmark_mask, "actual_avg_yield_ton_per_ha"]
        / efficiency_df.loc[valid_benchmark_mask, "avg_yield_benchmark_ton_per_ha"]
        * 100
    )

    efficiency_df = efficiency_df[
        [
            "crop_name",
            "crop_category",
            "avg_yield_benchmark_ton_per_ha",
            "actual_avg_yield_ton_per_ha",
            "efficiency_pct",
            "total_area_planted_ha",
            "crop_season",
        ]
    ].rename(columns={"crop_season": "season"})

    efficiency_df = (
        efficiency_df.sort_values(
            by=["efficiency_pct", "crop_name", "season"],
            ascending=[False, True, True],
        )
        .reset_index(drop=True)
    )

    efficiency_df = round_numeric_columns(efficiency_df, decimals=2)

    return {
        "filters_applied": build_filters_applied(
            {
                "crop_category": crop_category,
                "season": season,
                "year": year,
                "region": region,
                "water_requirement": water_requirement,
            }
        ),
        "data": dataframe_to_records(efficiency_df),
    }


def get_crop_seasonal_trend(
    *,
    crop_name: Optional[str] = None,
    crop_category: Optional[CropCategory] = None,
    year: Optional[Year] = None,
    quarter: Optional[Quarter] = None,
    market_type: Optional[MarketType] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /crops/seasonal-trend.

    Supported PRD filters:
        - crop_name
        - crop_category
        - year
        - quarter
        - market_type

    Notes:
        This endpoint uses harvest/calendar season from vw_harvest_full.season,
        not dim_crop.growing_season.
    """
    df = load_harvest_full()

    validate_required_columns(df, SEASONAL_TREND_REQUIRED_COLUMNS)

    filtered_df = apply_optional_filters(
        df,
        {
            "crop_name": crop_name,
            "crop_category": crop_category,
            "year": year,
            "quarter": quarter,
            "market_type": market_type,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No seasonal trend data found for the requested filters.",
    )

    trend_df = (
        filtered_df.groupby(
            ["crop_name", "year", "quarter", "season"],
            as_index=False,
        )
        .agg(
            total_quantity_sold_ton=("quantity_sold_ton", "sum"),
            total_revenue_bdt=("revenue_bdt", "sum"),
            avg_price_per_ton_bdt=("price_per_ton_bdt", "mean"),
            num_harvests=("harvest_id", "nunique"),
        )
        .sort_values(
            by=["year", "quarter", "crop_name"],
            ascending=[True, True, True],
        )
        .reset_index(drop=True)
    )

    trend_df = round_numeric_columns(trend_df, decimals=2)

    return {
        "filters_applied": build_filters_applied(
            {
                "crop_name": crop_name,
                "crop_category": crop_category,
                "year": year,
                "quarter": quarter,
                "market_type": market_type,
            }
        ),
        "trend": dataframe_to_records(trend_df),
    }


def get_crop_quality_breakdown(
    *,
    crop_id: Optional[int] = None,
    crop_category: Optional[CropCategory] = None,
    year: Optional[Year] = None,
    region: Optional[Region] = None,
    market_type: Optional[MarketType] = None,
    pesticide_residue: Optional[PesticideResidue] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /crops/quality-breakdown.

    Supported PRD filters:
        - crop_id
        - crop_category
        - year
        - region
        - market_type
        - pesticide_residue
    """
    df = load_harvest_full()

    df = load_harvest_full()



    harvest_df = load_harvest_full()
    crop_df = load_dim_crop()

    validate_required_columns(
        harvest_df,
        QUALITY_BREAKDOWN_HARVEST_REQUIRED_COLUMNS,
    )
    validate_required_columns(
        crop_df,
        QUALITY_BREAKDOWN_CROP_REQUIRED_COLUMNS,
    )

    crop_lookup_df = (
        crop_df[
            [
                "crop_id",
                "crop_name",
                "crop_category",
            ]
        ]
        .drop_duplicates()
    )

    df = harvest_df.merge(
        crop_lookup_df,
        on=["crop_name", "crop_category"],
        how="left",
    )

    if df["crop_id"].isna().any():
        raise ValueError("Some harvest records could not be matched to dim_crop.")

    filtered_df = apply_optional_filters(
        df,
        {
            "crop_id": crop_id,
            "crop_category": crop_category,
            "year": year,
            "region": region,
            "market_type": market_type,
            "pesticide_residue": pesticide_residue,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No crop quality breakdown data found for the requested filters.",
    )

    total_records = int(len(filtered_df))

    grade_distribution: dict[str, dict[str, float | int]] = {}

    for grade in QUALITY_GRADES:
        grade_df = filtered_df[filtered_df["quality_grade"] == grade]
        count = int(len(grade_df))
        pct = round((count / total_records) * 100, 2) if total_records else 0.0
        avg_revenue = (
            round(float(grade_df["revenue_bdt"].mean()), 2) if count > 0 else 0.0
        )

        grade_distribution[grade] = {
            "count": count,
            "pct": pct,
            "avg_revenue_bdt": avg_revenue,
        }

    pesticide_residue_breakdown: dict[str, dict[str, float | int]] = {}

    for residue_level in PESTICIDE_RESIDUE_LEVELS:
        residue_df = filtered_df[filtered_df["pesticide_residue"] == residue_level]
        count = int(len(residue_df))
        pct = round((count / total_records) * 100, 2) if total_records else 0.0

        pesticide_residue_breakdown[residue_level] = {
            "count": count,
            "pct": pct,
        }

    return {
        "filters_applied": build_filters_applied(
            {
                "crop_id": crop_id,
                "crop_category": crop_category,
                "year": year,
                "region": region,
                "market_type": market_type,
                "pesticide_residue": pesticide_residue,
            }
        ),
        "total_records": total_records,
        "grade_distribution": grade_distribution,
        "pesticide_residue_breakdown": pesticide_residue_breakdown,
    }