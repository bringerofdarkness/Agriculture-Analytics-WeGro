import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import get_connection


def main() -> None:
    with get_connection() as connection:
        df = pd.read_sql(
            text(
                """
                SELECT
                    crop_name,
                    crop_category,
                    growing_season
                FROM dim_crop
                ORDER BY crop_category, crop_name
                """
            ),
            connection,
        )

    print("=" * 88)
    print("dim_crop growing_season values")
    print("=" * 88)
    print(df.to_string(index=False))

    print()
    print("=" * 88)
    print("Unique growing_season values")
    print("=" * 88)
    print(sorted(df["growing_season"].dropna().unique().tolist()))


if __name__ == "__main__":
    main()