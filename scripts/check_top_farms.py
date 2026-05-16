from pprint import pprint

from app.enums import FarmType, RankingMetric, Region, Year
from app.services.farm_reports import get_top_farms_ranking


def main() -> None:
    print("Checking top farms with defaults...")
    default_result = get_top_farms_ranking()
    pprint(default_result)

    print()
    print("Checking top farms: metric=profit, region=Rajshahi, farm_type=Commercial, limit=5")
    filtered_result = get_top_farms_ranking(
        metric=RankingMetric.PROFIT,
        region=Region.RAJSHAHI,
        farm_type=FarmType.COMMERCIAL,
        limit=5,
    )
    pprint(filtered_result)

    print()
    print("Checking top farms: metric=revenue, year=2023, limit=3")
    revenue_result = get_top_farms_ranking(
        metric=RankingMetric.REVENUE,
        year=Year.YEAR_2023,
        limit=3,
    )
    pprint(revenue_result)

    print()
    print("Checking top farms: metric=yield, year=2024, limit=3")
    yield_result = get_top_farms_ranking(
        metric=RankingMetric.YIELD,
        year=Year.YEAR_2024,
        limit=3,
    )
    pprint(yield_result)


if __name__ == "__main__":
    main()