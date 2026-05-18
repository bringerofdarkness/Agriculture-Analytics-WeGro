from app.routers.crop_quality import router as crop_quality_router
from app.routers.crops import router as crops_router
from app.routers.farms import router as farms_router
from app.routers.markets import router as markets_router


__all__ = [
    "crop_quality_router",
    "crops_router",
    "farms_router",
    "markets_router",
]