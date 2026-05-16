from pprint import pprint

from app.enums import Region, Year
from app.services.farm_reports import get_farm_summary


def main() -> None:
    print("Checking farm summary without filters...")
    all_farms_result = get_farm_summary()
    pprint(all_farms_result)

    print()
    print("Checking farm summary with filters: region=Dhaka, year=2023")
    filtered_result = get_farm_summary(
        region=Region.DHAKA,
        year=Year.YEAR_2023,
    )
    pprint(filtered_result)


if __name__ == "__main__":
    main()