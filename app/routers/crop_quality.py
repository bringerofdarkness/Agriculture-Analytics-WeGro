from typing import Any
from fastapi import APIRouter

from app.schemas.crop_reports import CropQualityBreakdownResponse
from app.schemas.filters import (
    CropCategoryFilter,
    CropIdFilter,
    MarketTypeFilter,
    PesticideResidueFilter,
    RegionFilter,
    YearFilter,
)
from app.services.crop_reports import get_crop_quality_breakdown

router = APIRouter(
    prefix="/crops",
    tags=["Report 2 - Crop & Market Intelligence"],
)


@router.get(
    "/quality-breakdown",
    response_model=CropQualityBreakdownResponse,
    summary="Quality Grade Breakdown",
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
) -> dict[str, Any]:
    # Enforcing generic dict exchange to seamlessly pipe to response_model validator
    return get_crop_quality_breakdown(
        crop_id=crop_id,
        crop_category=crop_category,
        year=year,
        region=region,
        market_type=market_type,
        pesticide_residue=pesticide_residue,
    )