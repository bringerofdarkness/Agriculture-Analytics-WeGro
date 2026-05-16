from enum import Enum
from typing import Annotated, Any, Dict, Mapping, Optional

from fastapi import Path, Query

from app.enums import (
    CropCategory,
    FarmType,
    MarketType,
    PesticideResidue,
    PriceTier,
    QualityGrade,
    Quarter,
    RankingMetric,
    Region,
    Season,
    WaterRequirement,
    Year,
)


RegionFilter = Annotated[
    Optional[Region],
    Query(default=None, description="Filter by region."),
]

FarmTypeFilter = Annotated[
    Optional[FarmType],
    Query(default=None, description="Filter by farm type."),
]

YearFilter = Annotated[
    Optional[Year],
    Query(default=None, description="Filter by year."),
]

SeasonFilter = Annotated[
    Optional[Season],
    Query(default=None, description="Filter by season."),
]

CropCategoryFilter = Annotated[
    Optional[CropCategory],
    Query(default=None, description="Filter by crop category."),
]

MarketTypeFilter = Annotated[
    Optional[MarketType],
    Query(default=None, description="Filter by market type."),
]

QualityGradeFilter = Annotated[
    Optional[QualityGrade],
    Query(default=None, description="Filter by quality grade."),
]

PriceTierFilter = Annotated[
    Optional[PriceTier],
    Query(default=None, description="Filter by price tier."),
]

PesticideResidueFilter = Annotated[
    Optional[PesticideResidue],
    Query(default=None, description="Filter by pesticide residue level."),
]

WaterRequirementFilter = Annotated[
    Optional[WaterRequirement],
    Query(default=None, description="Filter by water requirement."),
]

QuarterFilter = Annotated[
    Optional[Quarter],
    Query(default=None, description="Filter by quarter. Accepted values: 1, 2, 3, 4."),
]

CropNameFilter = Annotated[
    Optional[str],
    Query(default=None, min_length=1, description="Filter by crop name."),
]

DistrictFilter = Annotated[
    Optional[str],
    Query(default=None, min_length=1, description="Filter by district."),
]

CropIdFilter = Annotated[
    Optional[int],
    Query(default=None, ge=1, description="Filter by crop ID."),
]

MetricFilter = Annotated[
    RankingMetric,
    Query(default=RankingMetric.PROFIT, description="Ranking metric."),
]

LimitFilter = Annotated[
    int,
    Query(default=10, ge=1, description="Any positive integer. Default: 10."),
]

FarmIdPath = Annotated[
    int,
    Path(description="Farm ID. PRD states farm_id is an integer from 1 to 30.", ge=1, le=30),
]


def serialize_filter_value(value: Any) -> Any:
    """
    Convert Enum values into clean JSON-compatible values.

    Example:
        Region.DHAKA -> "Dhaka"
        Year.YEAR_2023 -> 2023
    """
    if isinstance(value, Enum):
        return value.value

    return value


def build_filters_applied(filters: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Build the PRD-style filters_applied object.

    Only non-null filters should appear in the API response.
    """
    return {
        key: serialize_filter_value(value)
        for key, value in filters.items()
        if value is not None
    }