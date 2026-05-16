from enum import Enum
from typing import Any, Mapping

import pandas as pd

from app.exceptions import DataNotFoundError


def normalize_filter_value(value: Any) -> Any:
    """
    Convert enum values to their raw values for pandas comparison.

    Examples:
        Region.DHAKA -> "Dhaka"
        Year.YEAR_2023 -> 2023
    """
    if isinstance(value, Enum):
        return value.value

    return value


def validate_required_columns(df: pd.DataFrame, required_columns: set[str]) -> None:
    """
    Ensure all columns required for a transformation exist.

    This catches schema drift early and gives a clear developer-facing error.
    """
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required DataFrame columns: {missing}")


def ensure_dataframe_not_empty(
    df: pd.DataFrame,
    message: str = "No data found for the requested filters.",
) -> pd.DataFrame:
    """
    Raise a domain-specific error when a DataFrame has no rows.
    """
    if df.empty:
        raise DataNotFoundError(message)

    return df


def apply_optional_filters(
    df: pd.DataFrame,
    filters: Mapping[str, Any],
) -> pd.DataFrame:
    """
    Apply optional filters to a DataFrame using vectorised boolean indexing.

    Args:
        df: Source DataFrame.
        filters: Mapping where keys are DataFrame column names and values are
                 optional filter values.

    Returns:
        Filtered DataFrame.

    Notes:
        - None values are ignored.
        - Enum values are converted to their raw PRD-approved values.
        - A copy is returned to avoid accidental mutation downstream.
    """
    active_filters = {
        column: normalize_filter_value(value)
        for column, value in filters.items()
        if value is not None
    }

    if not active_filters:
        return df.copy()

    validate_required_columns(df, set(active_filters.keys()))

    mask = pd.Series(True, index=df.index)

    for column, value in active_filters.items():
        mask &= df[column].eq(value)

    return df.loc[mask].copy()


def round_numeric_columns(
    df: pd.DataFrame,
    decimals: int = 2,
) -> pd.DataFrame:
    """
    Round numeric columns for clean JSON responses.

    This keeps API output stable and avoids long floating-point artifacts.
    """
    rounded_df = df.copy()
    numeric_columns = rounded_df.select_dtypes(include=["number"]).columns

    rounded_df[numeric_columns] = rounded_df[numeric_columns].round(decimals)

    return rounded_df


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Convert a DataFrame into JSON-safe record dictionaries.

    pandas may produce NaN values, which are not ideal for JSON APIs.
    This converts missing values into None.
    """
    json_safe_df = df.where(pd.notna(df), None)

    return json_safe_df.to_dict(orient="records")