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