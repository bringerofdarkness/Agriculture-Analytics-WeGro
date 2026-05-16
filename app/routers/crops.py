from fastapi import APIRouter

from app.schemas.crop_reports import CropYieldEfficiencyResponse
from app.schemas.filters import (
    CropCategoryFilter,
    RegionFilter,
    SeasonFilter,
    WaterRequirementFilter,
    YearFilter,
)
from app.services.crop_reports import get_crop_yield_efficiency


router = APIRouter(
    prefix="/crops",
    tags=["Report 2 - Crop & Market Intelligence"],
)


@router.get(
    "/yield-efficiency",
    response_model=CropYieldEfficiencyResponse,
    summary="Crop Yield Efficiency",
    description=(
        "Compares actual yield per hectare against benchmark yield for each crop. "
        "Supports filtering by crop_category, season, year, region, and "
        "water_requirement."
    ),
)
def read_crop_yield_efficiency(
    crop_category: CropCategoryFilter = None,
    season: SeasonFilter = None,
    year: YearFilter = None,
    region: RegionFilter = None,
    water_requirement: WaterRequirementFilter = None,
) -> CropYieldEfficiencyResponse:
    return get_crop_yield_efficiency(
        crop_category=crop_category,
        season=season,
        year=year,
        region=region,
        water_requirement=water_requirement,
    )