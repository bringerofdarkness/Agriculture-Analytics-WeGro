from typing import Any, Optional

from app.enums import CropCategory, MarketType, PriceTier, Season, Year
from app.schemas.filters import build_filters_applied
from app.services.data_loader import load_dim_market, load_harvest_full
from app.services.dataframe_utils import (
    apply_optional_filters,
    dataframe_to_records,
    ensure_dataframe_not_empty,
    round_numeric_columns,
    validate_required_columns,
)


MARKET_PRICE_COMPARISON_HARVEST_REQUIRED_COLUMNS: set[str] = {
    "market_name",
    "market_type",
    "price_tier",
    "crop_name",
    "crop_category",
    "year",
    "season",
    "price_per_ton_bdt",
    "quantity_sold_ton",
    "revenue_bdt",
}

MARKET_PRICE_COMPARISON_MARKET_REQUIRED_COLUMNS: set[str] = {
    "market_name",
    "market_type",
    "price_tier",
    "district",
}


def get_market_price_comparison(
    *,
    market_type: Optional[MarketType] = None,
    crop_category: Optional[CropCategory] = None,
    year: Optional[Year] = None,
    season: Optional[Season] = None,
    price_tier: Optional[PriceTier] = None,
    district: Optional[str] = None,
) -> dict[str, Any]:
    """
    Build the PRD response body for GET /markets/price-comparison.

    Supported PRD filters:
        - market_type
        - crop_category
        - year
        - season
        - price_tier
        - district

    Notes:
        The response district must come from dim_market.district.
        vw_harvest_full.farm_district is the farm district, not the market district.
    """
    harvest_df = load_harvest_full()
    market_df = load_dim_market()

    validate_required_columns(
        harvest_df,
        MARKET_PRICE_COMPARISON_HARVEST_REQUIRED_COLUMNS,
    )
    validate_required_columns(
        market_df,
        MARKET_PRICE_COMPARISON_MARKET_REQUIRED_COLUMNS,
    )

    market_lookup_df = (
        market_df[
            [
                "market_name",
                "market_type",
                "price_tier",
                "district",
            ]
        ]
        .drop_duplicates()
        .rename(columns={"district": "market_district"})
    )

    df = harvest_df.merge(
        market_lookup_df,
        on=["market_name", "market_type", "price_tier"],
        how="left",
    )

    if df["market_district"].isna().any():
        raise ValueError("Some harvest records could not be matched to dim_market.")

    filtered_df = apply_optional_filters(
        df,
        {
            
            "crop_category": crop_category,
            "year": year,
            "season": season,
            "market_type": market_type,
            "price_tier": price_tier,
            "market_district": district,
        },
    )

    ensure_dataframe_not_empty(
        filtered_df,
        "No market price comparison data found for the requested filters.",
    )

    comparison_df = (
        filtered_df.groupby(
            [
                "market_name",
                "market_type",
                "price_tier",
                "market_district",
                "crop_name",
            ],
            as_index=False,
        )
        .agg(
            avg_price_per_ton_bdt=("price_per_ton_bdt", "mean"),
            total_quantity_sold_ton=("quantity_sold_ton", "sum"),
            total_revenue_bdt=("revenue_bdt", "sum"),
        )
        .rename(columns={"market_district": "district"})
        .sort_values(
            by=[
                "avg_price_per_ton_bdt",
                "total_revenue_bdt",
                "market_name",
                "crop_name",
            ],
            ascending=[False, False, True, True],
        )
        .reset_index(drop=True)
    )

    comparison_df = comparison_df[
        [
            "market_name",
            "market_type",
            "price_tier",
            "district",
            "crop_name",
            "avg_price_per_ton_bdt",
            "total_quantity_sold_ton",
            "total_revenue_bdt",
        ]
    ]

    comparison_df = round_numeric_columns(comparison_df, decimals=2)

    return {
        "filters_applied": build_filters_applied(
            {
                
                "crop_category": crop_category,
                "year": year,
                "season": season,
                "market_type": market_type,
                "price_tier": price_tier,
                "district": district,
            }
        ),
        "comparison": dataframe_to_records(comparison_df),
    }