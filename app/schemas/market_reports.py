from typing import Any

from pydantic import BaseModel, ConfigDict


class MarketPriceComparisonItem(BaseModel):
    market_name: str
    market_type: str
    price_tier: str
    district: str
    crop_name: str
    avg_price_per_ton_bdt: float
    total_quantity_sold_ton: float
    total_revenue_bdt: float


class MarketPriceComparisonResponse(BaseModel):
    filters_applied: dict[str, Any]
    comparison: list[MarketPriceComparisonItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filters_applied": {
                    "crop_category": "Cereal",
                    "year": 2023,
                    "market_type": "Export",
                },
                "comparison": [
                    {
                        "market_name": "Chittagong Port Market",
                        "market_type": "Export",
                        "price_tier": "Premium",
                        "district": "Chittagong",
                        "crop_name": "Aman Rice",
                        "avg_price_per_ton_bdt": 48000,
                        "total_quantity_sold_ton": 87.0,
                        "total_revenue_bdt": 4176000,
                    }
                ],
            }
        }
    )