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
                        "total_revenue_bdt": 8624000,
                        "avg_price_per_ton_bdt": 22000,
                        "num_harvests": 4,
                    }
                ],
            }
        }
    )