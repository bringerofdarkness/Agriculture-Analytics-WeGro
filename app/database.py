import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


def build_mysql_url(settings: Settings) -> URL:
    """
    Build SQLAlchemy MySQL URL safely.

    URL.create handles special characters in passwords correctly.
    """
    return URL.create(
        drivername="mysql+pymysql",
        username=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        host=settings.mysql_host,
        port=settings.mysql_port,
        database=settings.mysql_database,
    )


def create_db_engine(settings: Settings) -> Engine:
    return create_engine(
        build_mysql_url(settings),
        pool_pre_ping=True,
        pool_recycle=settings.db_pool_recycle_seconds,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        echo=settings.db_echo,
        future=True,
    )


settings = get_settings()
engine = create_db_engine(settings)


@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    connection = engine.connect()

    try:
        yield connection
    except SQLAlchemyError:
        logger.exception("Database operation failed.")
        raise
    finally:
        connection.close()


def ping_database() -> bool:
    with get_connection() as connection:
        connection.execute(text("SELECT 1")).scalar_one()

    return True


def dispose_engine() -> None:
    engine.dispose()