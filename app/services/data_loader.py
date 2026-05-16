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


ALLOWED_VIEWS: Final[set[str]] = {view.value for view in DatabaseView}


def validate_view_name(view_name: str) -> None:
    """
    Guard against unsafe or unsupported table/view access.

    We never interpolate user-controlled table names unless they are explicitly
    allowlisted.
    """
    if view_name not in ALLOWED_VIEWS:
        allowed = ", ".join(sorted(ALLOWED_VIEWS))
        raise ValueError(f"Unsupported database view '{view_name}'. Allowed: {allowed}")


def load_view_as_dataframe(view: DatabaseView) -> pd.DataFrame:
    """
    Load a full PRD-approved database view into a pandas DataFrame.

    This is the foundation for endpoint-level pandas transformations.
    """
    validate_view_name(view.value)

    query = text(f"SELECT * FROM {view.value}")

    with get_connection() as connection:
        return pd.read_sql(query, connection)


def load_harvest_full() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.HARVEST_FULL)


def load_revenue_by_crop_year() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.REVENUE_BY_CROP_YEAR)


def load_farm_profitability() -> pd.DataFrame:
    return load_view_as_dataframe(DatabaseView.FARM_PROFITABILITY)