from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


# REPORT 1: ENDPOINT 1 (Farms Summary) ---
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
                        "total_revenue_bdt": 4250000.0,
                        "total_cost_bdt": 980000.0,
                        "net_profit_bdt": 3270000.0,
                        "avg_loss_pct": 4.2,
                    }
                ],
            }
        }
    )


# REPORT 1: ENDPOINT 2 (Single Farm Performance) ---
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
                        "revenue_bdt": 1560000.0,
                        "net_profit_bdt": 1180000.0,
                        "quality_grade": "A",
                    }
                ],
            }
        }
    )


# REPORT 1: ENDPOINT 3 (Top Farms Ranking) ---
class TopFarmRankingItem(BaseModel):
    rank: int
    farm_name: str
    region: str
    farm_type: str
    net_profit_bdt: float
    total_revenue_bdt: float


class TopFarmsRankingResponse(BaseModel):
    metric: str
    filters_applied: dict[str, Any]
    rankings: list[TopFarmRankingItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metric": "profit",
                "filters_applied": {
                    "region": "Rajshahi",
                    "farm_type": "Commercial",
                    "limit": 5,
                },
                "rankings": [
                    {
                        "rank": 1,
                        "farm_name": "Barind Farms",
                        "region": "Rajshahi",
                        "farm_type": "Commercial",
                        "net_profit_bdt": 8900000.0,
                        "total_revenue_bdt": 11200000.0,
                    }
                ],
            }
        }
    )


# REPORT 1: ENDPOINT 4 (Farm Loss Analysis) ---
class LossAnalysisSummary(BaseModel):
    total_harvested_ton: float
    total_lost_ton: float
    overall_loss_pct: float


class LossAnalysisBreakdownItem(BaseModel):
    region: str
    crop_category: str
    quality_grade: str
    total_lost_ton: float
    loss_pct: float
    pesticide_residue: str


class FarmLossAnalysisResponse(BaseModel):
    filters_applied: dict[str, Any]
    summary: LossAnalysisSummary
    breakdown: list[LossAnalysisBreakdownItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filters_applied": {
                    "season": "Kharif",
                    "year": 2023,
                    "quality_grade": "C",
                },
                "summary": {
                    "total_harvested_ton": 1240.5,
                    "total_lost_ton": 98.2,
                    "overall_loss_pct": 7.9,
                },
                "breakdown": [
                    {
                        "region": "Chittagong",
                        "crop_category": "Cereal",
                        "quality_grade": "C",
                        "total_lost_ton": 42.5,
                        "loss_pct": 9.1,
                        "pesticide_residue": "Trace",
                    }
                ],
            }
        }
    )