from fastapi import APIRouter

from app.schemas.crop_reports import (
    CropQualityBreakdownResponse,
    CropSeasonalTrendResponse,
    CropYieldEfficiencyResponse,
)
from app.schemas.filters import (
    CropCategoryFilter,
    CropIdFilter,
    CropNameFilter,
    MarketTypeFilter,
    PesticideResidueFilter,
    QuarterFilter,
    RegionFilter,
    SeasonFilter,
    WaterRequirementFilter,
    YearFilter,
)

from app.services.crop_reports import (
    get_crop_quality_breakdown,
    get_crop_seasonal_trend,
    get_crop_yield_efficiency,
)


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


@router.get(
    "/seasonal-trend",
    response_model=CropSeasonalTrendResponse,
    summary="Seasonal Revenue Trend",
    description=(
        "Shows how revenue and quantity sold change across different seasons "
        "and years for each crop. Supports filtering by crop_name, "
        "crop_category, year, quarter, and market_type."
    ),
)
def read_crop_seasonal_trend(
    crop_name: CropNameFilter = None,
    crop_category: CropCategoryFilter = None,
    year: YearFilter = None,
    quarter: QuarterFilter = None,
    market_type: MarketTypeFilter = None,
) -> CropSeasonalTrendResponse:
    return get_crop_seasonal_trend(
        crop_name=crop_name,
        crop_category=crop_category,
        year=year,
        quarter=quarter,
        market_type=market_type,
    )


@router.get(
    "/quality-breakdown",
    response_model=CropQualityBreakdownResponse,
    summary="Crop Quality Breakdown",
    description=(
        "Shows quality grade distribution and pesticide residue breakdown "
        "for crop harvest records. Supports filtering by crop_id, "
        "crop_category, year, region, market_type, and pesticide_residue."
    ),
)
def read_crop_quality_breakdown(
    crop_id: CropIdFilter = None,
    crop_category: CropCategoryFilter = None,
    year: YearFilter = None,
    region: RegionFilter = None,
    market_type: MarketTypeFilter = None,
    pesticide_residue: PesticideResidueFilter = None,
) -> CropQualityBreakdownResponse:
    return get_crop_quality_breakdown(
        crop_id=crop_id,
        crop_category=crop_category,
        year=year,
        region=region,
        market_type=market_type,
        pesticide_residue=pesticide_residue,
    )