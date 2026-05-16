from typing import Any

from pydantic import BaseModel, ConfigDict


class FarmSummaryItem(BaseModel):
    farm_name: str
    region: str
    farm_type: str
    total_revenue_bdt: float
    total_cost_bdt: float
    net_profit_bdt: float
    avg_loss_pct: float


class FarmSummaryResponse(BaseModel):
    total_farms: int
    filters_applied: dict[str, Any]
    data: list[FarmSummaryItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_farms": 12,
                "filters_applied": {
                    "region": "Dhaka",
                    "year": 2023,
                },
                "data": [
                    {
                        "farm_name": "Green Valley Farm",
                        "region": "Dhaka",
                        "farm_type": "Large",
                        "total_revenue_bdt": 4250000,
                        "total_cost_bdt": 980000,
                        "net_profit_bdt": 3270000,
                        "avg_loss_pct": 4.2,
                    }
                ],
            }
        }
    )


class SingleFarmPerformanceItem(BaseModel):
    crop_name: str
    year: int
    market_type: str
    quantity_sold_ton: float
    revenue_bdt: float
    net_profit_bdt: float
    quality_grade: str


class SingleFarmPerformanceResponse(BaseModel):
    farm_id: int
    farm_name: str
    owner: str
    region: str
    filters_applied: dict[str, Any]
    performance: list[SingleFarmPerformanceItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "farm_id": 1,
                "farm_name": "Green Valley Farm",
                "owner": "Rahman Ali",
                "region": "Dhaka",
                "filters_applied": {
                    "year": 2023,
                    "crop_category": "Cereal",
                },
                "performance": [
                    {
                        "crop_name": "Boro Rice",
                        "year": 2023,
                        "market_type": "Wholesale",
                        "quantity_sold_ton": 60.0,
                        "revenue_bdt": 1560000,
                        "net_profit_bdt": 1180000,
                        "quality_grade": "A",
                    }
                ],
            }
        }
    )