from fastapi import APIRouter

from app.schemas.farm_reports import (
    FarmSummaryResponse,
    SingleFarmPerformanceResponse,
)
from app.schemas.filters import (
    CropCategoryFilter,
    FarmIdPath,
    FarmTypeFilter,
    MarketTypeFilter,
    RegionFilter,
    SeasonFilter,
    YearFilter,
)
from app.services.farm_reports import get_farm_summary, get_single_farm_performance


router = APIRouter(
    prefix="/farms",
    tags=["Report 1 - Farm Performance"],
)


@router.get(
    "/summary",
    response_model=FarmSummaryResponse,
    summary="Farm Summary",
    description=(
        "Returns a summary of all farms with total revenue, total profit, "
        "total cost, and average loss percentage. Supports filtering by "
        "region, farm_type, year, and season."
    ),
)
def read_farm_summary(
    region: RegionFilter = None,
    farm_type: FarmTypeFilter = None,
    year: YearFilter = None,
    season: SeasonFilter = None,
) -> FarmSummaryResponse:
    return get_farm_summary(
        region=region,
        farm_type=farm_type,
        year=year,
        season=season,
    )


@router.get(
    "/{farm_id}/performance",
    response_model=SingleFarmPerformanceResponse,
    summary="Single Farm Performance",
    description=(
        "Returns detailed performance for one specific farm, including "
        "revenue and profit per crop, year, and market channel. Supports "
        "filtering by year, crop_category, and market_type."
    ),
)
def read_single_farm_performance(
    farm_id: FarmIdPath,
    year: YearFilter = None,
    crop_category: CropCategoryFilter = None,
    market_type: MarketTypeFilter = None,
) -> SingleFarmPerformanceResponse:
    return get_single_farm_performance(
        farm_id=farm_id,
        year=year,
        crop_category=crop_category,
        market_type=market_type,
    )