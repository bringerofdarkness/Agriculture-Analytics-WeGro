from pprint import pprint

from app.enums import CropCategory, MarketType, Year
from app.services.farm_reports import get_single_farm_performance


def main() -> None:
    print("Checking farm_id=1 without filters...")
    result = get_single_farm_performance(farm_id=1)
    pprint(result)

    print()
    print("Checking farm_id=1 with filters: year=2023, crop_category=Cereal")
    filtered_result = get_single_farm_performance(
        farm_id=1,
        year=Year.YEAR_2023,
        crop_category=CropCategory.CEREAL,
    )
    pprint(filtered_result)

    print()
    print("Checking farm_id=1 with filters: market_type=Wholesale")
    market_result = get_single_farm_performance(
        farm_id=1,
        market_type=MarketType.WHOLESALE,
    )
    pprint(market_result)


if __name__ == "__main__":
    main()