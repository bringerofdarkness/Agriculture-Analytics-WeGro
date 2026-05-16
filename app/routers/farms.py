from app.enums import FarmType, Region, Season, Year
from app.schemas.farm_reports import FarmSummaryResponse
from app.schemas.filters import (
    FarmTypeFilter,
    RegionFilter,
    SeasonFilter,
    YearFilter,
)
from app.services.farm_reports import get_farm_summary
from fastapi import APIRouter


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