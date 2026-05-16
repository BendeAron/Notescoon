from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import sessionmaker
from starlette.exceptions import HTTPException as StarletteHTTPException

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


# --- Frontend serving (production / built assets) ---
# Vite build output lives at repo-root `dist/`.
REPO_ROOT = Path(__file__).resolve().parents[3]
DIST_DIR = REPO_ROOT / "dist"
INDEX_FILE = DIST_DIR / "index.html"

if DIST_DIR.is_dir() and INDEX_FILE.is_file():
    logger.info("Serving frontend from dist", extra={"dist": str(DIST_DIR)})
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")


@app.exception_handler(StarletteHTTPException)
async def http_exception_spa_fallback(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404 and DIST_DIR.is_dir() and INDEX_FILE.is_file():
        path = request.url.path
        if not path.startswith("/api") and path != "/health":
            # Only SPA-fallback for routes without a file extension.
            if "." not in Path(path).name:
                accept = request.headers.get("accept", "")
                if "text/html" in accept or accept in {"", "*/*"}:
                    from fastapi.responses import FileResponse

                    return FileResponse(INDEX_FILE)

    return await http_exception_handler(request, exc)
