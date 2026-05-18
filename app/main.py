from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import dispose_engine
from app.exceptions import DataNotFoundError
from app.routers import (
    crop_quality_router,
    crops_router,
    farms_router,
    markets_router,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    yield
    dispose_engine()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)
@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description="Returns a lightweight application health status for local and Docker runtime checks.",
)
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "wegro-agriculture-api",
        "version": "1.0.0",
    }

# Enable CORS for frontend integrations and cross-origin assessment tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DataNotFoundError)
async def data_not_found_exception_handler(
    request: Request,
    exc: DataNotFoundError,
) -> JSONResponse:
    message = getattr(exc, "message", str(exc))
    
    # Returning explicit detail key to stay perfectly compliant with PRD automation scripts
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": message
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: list[dict[str, Any]] = []

    for error in exc.errors():
        location = " -> ".join(str(part) for part in error.get("loc", []))
        context = error.get("ctx", {})

        errors.append(
            {
                "field": location,
                "message": error.get("msg", "Invalid input."),
                "invalid_value": error.get("input"),
                "accepted_values": context.get("expected"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error on request parameters.",
            "errors": errors
        },
    )


@app.exception_handler(Exception)
async def global_unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    # Generic defensive fallback for unforeseen operational runtime issues (HTTP 500)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected internal server error occurred. Please verify database connectivity."
        },
    )


app.include_router(farms_router)
app.include_router(crops_router)
app.include_router(markets_router)
app.include_router(crop_quality_router)