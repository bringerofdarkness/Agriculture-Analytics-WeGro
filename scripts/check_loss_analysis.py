from pprint import pprint

from app.enums import QualityGrade, Region, Season, Year
from app.services.farm_reports import get_farm_loss_analysis


def main() -> None:
    print("Checking loss analysis without filters...")
    default_result = get_farm_loss_analysis()
    pprint(default_result)

    print()
    print("Checking loss analysis: season=Winter, year=2023, quality_grade=A")
    filtered_result = get_farm_loss_analysis(
        season=Season.WINTER,
        year=Year.YEAR_2023,
        quality_grade=QualityGrade.A,
    )
    pprint(filtered_result)

    print()
    print("Checking loss analysis: region=Dhaka, year=2024")
    region_result = get_farm_loss_analysis(
        region=Region.DHAKA,
        year=Year.YEAR_2024,
    )
    pprint(region_result)


if __name__ == "__main__":
    main()