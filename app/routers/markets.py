from fastapi import APIRouter

from app.schemas.filters import (
    CropCategoryFilter,
    DistrictFilter,
    MarketTypeFilter,
    PriceTierFilter,
    SeasonFilter,
    YearFilter,
)
from app.schemas.market_reports import MarketPriceComparisonResponse
from app.services.market_reports import get_market_price_comparison


router = APIRouter(
    prefix="/markets",
    tags=["Report 2 - Crop & Market Intelligence"],
)


@router.get(
    "/price-comparison",
    response_model=MarketPriceComparisonResponse,
    summary="Market Price Comparison",
    description=(
        "Compares average selling prices across market types, districts, "
        "and price tiers for each crop. Supports filtering by market_type, "
        "crop_category, year, season, price_tier, and district."
    ),
)
def read_market_price_comparison(
    market_type: MarketTypeFilter = None,
    crop_category: CropCategoryFilter = None,
    year: YearFilter = None,
    season: SeasonFilter = None,
    price_tier: PriceTierFilter = None,
    district: DistrictFilter = None,
) -> MarketPriceComparisonResponse:
    return get_market_price_comparison(
        market_type=market_type,
        crop_category=crop_category,
        year=year,
        season=season,
        price_tier=price_tier,
        district=district,
    )