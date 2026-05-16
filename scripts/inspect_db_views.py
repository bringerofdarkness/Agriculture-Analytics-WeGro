import pandas as pd

from app.services import (
    DatabaseView,
    load_farm_profitability,
    load_harvest_full,
    load_revenue_by_crop_year,
)


def print_dataframe_profile(view_name: str, df: pd.DataFrame) -> None:
    print("=" * 80)
    print(f"VIEW: {view_name}")
    print("=" * 80)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print()

    print("Column names:")
    for column in df.columns:
        print(f"  - {column}")

    print()
    print("Dtypes:")
    print(df.dtypes)

    print()
    print("Null counts:")
    print(df.isna().sum())

    print()


def main() -> None:
    view_loaders = {
        DatabaseView.HARVEST_FULL.value: load_harvest_full,
        DatabaseView.REVENUE_BY_CROP_YEAR.value: load_revenue_by_crop_year,
        DatabaseView.FARM_PROFITABILITY.value: load_farm_profitability,
    }

    for view_name, loader in view_loaders.items():
        df = loader()
        print_dataframe_profile(view_name=view_name, df=df)


if __name__ == "__main__":
    main()