from enum import Enum
from typing import Final

import pandas as pd
from sqlalchemy import text

from app.database import get_connection


class DatabaseView(str, Enum):
    """
    PRD-recommended database views used for analytics processing.
    """

    HARVEST_FULL = "vw_harvest_full"
    REVENUE_BY_CROP_YEAR = "vw_revenue_by_crop_year"
    FARM_PROFITABILITY = "vw_farm_profitability"


class DatabaseTable(str, Enum):
    """
    PRD dimension tables required when a view does not expose needed keys.
    """

    DIM_FARM = "dim_farm"


ALLOWED_VIEWS: Final[set[str]] = {view.value for view in DatabaseView}
ALLOWED_TABLES: Final[set[str]] = {table.value for table in DatabaseTable}
ALLOWED_READ_SOURCES: Final[set[str]] = ALLOWED_VIEWS | ALLOWED_TABLES


def validate_read_source_name(source_name: str) -> None:
    """
    Guard against unsafe or unsupported table/view access.

    We never interpolate dynamic table names unless they are explicitly
    allowlisted.
    """
    if source_name not in ALLOWED_READ_SOURCES:
        allowed = ", ".join(sorted(ALLOWED_READ_SOURCES))
        raise ValueError(
            f"Unsupported database read source '{source_name}'. Allowed: {allowed}"
        )


def load_source_as_dataframe(source_name: str) -> pd.DataFrame:
    """
    Load an allowlisted database table or view into a pandas DataFrame.
    """
    validate_read_source_name(source_name)

    query = text(f"SELECT * FROM {source_name}")

    with get_connection() as connection:
        return pd.read_sql(query, connection)


def load_view_as_dataframe(view: DatabaseView) -> pd.DataFrame:
    """
    Load a full PRD-approved database view into a pandas DataFrame.
    """
    return load_source_as_dataframe(view.value)


def load_table_as_dataframe(table: DatabaseTable) -> pd.DataFrame:
    """
    Load a PRD-approved dimension table into a pandas DataFrame.
    """
    return load_source_as_dataframe(table.value)


def load_harvest_full() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.HARVEST_FULL)


def load_revenue_by_crop_year() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.REVENUE_BY_CROP_YEAR)


def load_farm_profitability() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.FARM_PROFITABILITY)


def load_dim_farm() -> pd.DataFrame:
    return load_table_as_dataframe(DatabaseTable.DIM_FARM)