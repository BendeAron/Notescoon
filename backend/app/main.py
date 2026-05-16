from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

from app.api.router import api_router
from app.core.config import get_settings
from app.core.errors import ApiError
from app.core.logging import configure_logging
from app.db.engine import check_db_connection, create_db_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings.log_level)

    logger.info("Starting Notescoon backend", extra={"env": settings.env})

    engine = create_db_engine(settings.database_url)
    try:
        check_db_connection(engine)
        logger.info("Database connection OK")
    except Exception:
        logger.exception("Database connection failed")
        raise

    app.state.settings = settings
    app.state.db_engine = engine
    app.state.db_sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)

    yield

    engine.dispose()
    logger.info("Shutdown complete")


app = FastAPI(title="Notescoon", lifespan=lifespan)


@app.exception_handler(ApiError)
async def api_error_handler(_request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


app.include_router(api_router, prefix="/api")


@app.get("/health")
def health():
    try:
        check_db_connection(app.state.db_engine)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": {"code": "db_unavailable", "message": "Database unavailable"},
            },
        )

    return {"status": "ok"}
