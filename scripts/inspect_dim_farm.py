import pandas as pd

from app.services import load_dim_farm


def print_dataframe_profile(df: pd.DataFrame) -> None:
    print("=" * 80)
    print("TABLE: dim_farm")
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
    print("First 10 rows:")
    print(df.head(10).to_dict(orient="records"))


def main() -> None:
    df = load_dim_farm()
    print_dataframe_profile(df)


if __name__ == "__main__":
    main()