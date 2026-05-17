import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.enums import CropCategory, MarketType, PriceTier, Year
from app.services.market_reports import get_market_price_comparison


def print_case(title: str, payload: dict[str, Any]) -> None:
    print("=" * 88)
    print(title)
    print("=" * 88)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    print()


def main() -> None:
    print_case(
        "Case 1: No filters",
        get_market_price_comparison(),
    )

    print_case(
        "Case 2: crop_category=Cereal, year=2023, market_type=Wholesale",
        get_market_price_comparison(
            crop_category=CropCategory.CEREAL,
            year=Year.YEAR_2023,
            market_type=MarketType.WHOLESALE,
        ),
    )

    print_case(
        "Case 3: price_tier=Premium",
        get_market_price_comparison(
            price_tier=PriceTier.PREMIUM,
        ),
    )

    print_case(
        "Case 4: district=Chittagong",
        get_market_price_comparison(
            district="Chittagong",
        ),
    )


if __name__ == "__main__":
    main()