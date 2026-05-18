from typing import Any
from pydantic import BaseModel, ConfigDict


class CropYieldEfficiencyItem(BaseModel):
    crop_name: str
    crop_category: str
    avg_yield_benchmark_ton_per_ha: float
    actual_avg_yield_ton_per_ha: float
    efficiency_pct: float
    total_area_planted_ha: float
    season: str


class CropSeasonalTrendItem(BaseModel):
    crop_name: str
    year: int
    quarter: int
    season: str
    total_quantity_sold_ton: float
    total_revenue_bdt: float
    avg_price_per_ton_bdt: float
    num_harvests: int


class CropYieldEfficiencyResponse(BaseModel):
    filters_applied: dict[str, Any]
    data: list[CropYieldEfficiencyItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filters_applied": {
                    "crop_category": "Cereal",
                    "year": 2023,
                },
                "data": [
                    {
                        "crop_name": "Boro Rice",
                        "crop_category": "Cereal",
                        "avg_yield_benchmark_ton_per_ha": 5.2,
                        "actual_avg_yield_ton_per_ha": 5.8,
                        "efficiency_pct": 111.5,
                        "total_area_planted_ha": 186.0,
                        "season": "Rabi",
                    }
                ],
            }
        }
    )


class CropSeasonalTrendResponse(BaseModel):
    filters_applied: dict[str, Any]
    trend: list[CropSeasonalTrendItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filters_applied": {
                    "crop_category": "Vegetable",
                    "year": 2023,
                },
                "trend": [
                    {
                        "crop_name": "Potato",
                        "year": 2023,
                        "quarter": 1,
                        "season": "Winter",
                        "total_quantity_sold_ton": 392.0,
                        "total_revenue_bdt": 8624000.0,
                        "avg_price_per_ton_bdt": 22000.0,
                        "num_harvests": 4,
                    }
                ],
            }
        }
    )


class QualityMetric(BaseModel):
    count: int
    pct: float


class QualityGradeMetric(QualityMetric):
    avg_revenue_bdt: float


class CropQualityBreakdownResponse(BaseModel):
    filters_applied: dict[str, Any]
    total_records: int
    grade_distribution: dict[str, QualityGradeMetric]
    pesticide_residue_breakdown: dict[str, QualityMetric]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filters_applied": {
                    "crop_category": "Vegetable",
                    "year": 2023,
                },
                "total_records": 13,
                "grade_distribution": {
                    "A": {
                        "count": 10,
                        "pct": 76.92,
                        "avg_revenue_bdt": 3274975.0,
                    },
                    "B": {
                        "count": 3,
                        "pct": 23.08,
                        "avg_revenue_bdt": 3121833.33,
                    },
                    "C": {
                        "count": 0,
                        "pct": 0.0,
                        "avg_revenue_bdt": 0.0,
                    },
                    "D": {
                        "count": 0,
                        "pct": 0.0,
                        "avg_revenue_bdt": 0.0,
                    },
                },
                "pesticide_residue_breakdown": {
                    "None": {
                        "count": 9,
                        "pct": 69.23,
                    },
                    "Trace": {
                        "count": 4,
                        "pct": 30.77,
                    },
                    "Low": {
                        "count": 0,
                        "pct": 0.0,
                    },
                    "High": {
                        "count": 0,
                        "pct": 0.0,
                    },
                },
            }
        }
    )