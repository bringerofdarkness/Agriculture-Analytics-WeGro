import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.enums import CropCategory, MarketType, PesticideResidue, Year
from app.services.crop_reports import get_crop_quality_breakdown


def print_case(title: str, payload: dict[str, Any]) -> None:
    print("=" * 88)
    print(title)
    print("=" * 88)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    print()


def main() -> None:
    print_case(
        "Case 1: No filters",
        get_crop_quality_breakdown(),
    )

    print_case(
        "Case 2: crop_category=Vegetable, year=2023",
        get_crop_quality_breakdown(
            crop_category=CropCategory.VEGETABLE,
            year=Year.YEAR_2023,
        ),
    )

    print_case(
        "Case 3: market_type=Wholesale",
        get_crop_quality_breakdown(
            market_type=MarketType.WHOLESALE,
        ),
    )

    print_case(
        "Case 4: pesticide_residue=Trace",
        get_crop_quality_breakdown(
            pesticide_residue=PesticideResidue.TRACE,
        ),
    )


if __name__ == "__main__":
    main()