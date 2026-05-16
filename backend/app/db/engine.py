from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def create_db_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def check_db_connection(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
