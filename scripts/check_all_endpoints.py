import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.crop_reports import (
    get_crop_quality_breakdown,
    get_crop_seasonal_trend,
    get_crop_yield_efficiency,
)
from app.services.farm_reports import (
    get_farm_loss_analysis,
    get_farm_summary,
    get_single_farm_performance,
    get_top_farms_ranking,
)
from app.services.market_reports import get_market_price_comparison


def print_case(title: str, payload: dict[str, Any]) -> None:
    print("=" * 100)
    print(title)
    print("=" * 100)
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
    print()


def main() -> None:
    print_case("Farm summary", get_farm_summary())

    print_case("Single farm performance: farm_id=1", get_single_farm_performance(farm_id=1))

    print_case("Top farms ranking", get_top_farms_ranking())

    print_case("Farm loss analysis", get_farm_loss_analysis())

    print_case("Crop yield efficiency", get_crop_yield_efficiency())

    print_case("Crop seasonal trend", get_crop_seasonal_trend())

    print_case("Market price comparison", get_market_price_comparison())

    print_case("Crop quality breakdown", get_crop_quality_breakdown())


if __name__ == "__main__":
    main()