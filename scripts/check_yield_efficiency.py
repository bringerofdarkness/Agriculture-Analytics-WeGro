from pprint import pprint

from app.enums import CropCategory, Region, WaterRequirement, Year
from app.services.crop_reports import get_crop_yield_efficiency


def main() -> None:
    print("Checking yield efficiency without filters...")
    default_result = get_crop_yield_efficiency()
    pprint(default_result)

    print()
    print("Checking yield efficiency: crop_category=Cereal, year=2023")
    filtered_result = get_crop_yield_efficiency(
        crop_category=CropCategory.CEREAL,
        year=Year.YEAR_2023,
    )
    pprint(filtered_result)

    print()
    print("Checking yield efficiency: region=Dhaka, water_requirement=High")
    region_result = get_crop_yield_efficiency(
        region=Region.DHAKA,
        water_requirement=WaterRequirement.HIGH,
    )
    pprint(region_result)


if __name__ == "__main__":
    main()