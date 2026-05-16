from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import dispose_engine
from app.exceptions import DataNotFoundError
from app.routers import crops_router, farms_router


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


@app.exception_handler(DataNotFoundError)
async def data_not_found_exception_handler(
    _: Request,
    exc: DataNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


app.include_router(farms_router)
app.include_router(crops_router)