import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app


client = TestClient(app)


SUCCESS_CASES: list[tuple[str, str, set[str]]] = [
    (
        "Farm summary",
        "/farms/summary",
        {"total_farms", "filters_applied", "data"},
    ),
    (
        "Single farm performance",
        "/farms/1/performance",
        {"farm_id", "farm_name", "owner", "region", "filters_applied", "performance"},
    ),
    (
        "Top farms ranking",
        "/farms/top?metric=profit&limit=10",
        {"metric", "filters_applied", "rankings"},
    ),
    (
        "Farm loss analysis",
        "/farms/loss-analysis",
        {"filters_applied", "summary", "breakdown"},
    ),
    (
        "Crop yield efficiency",
        "/crops/yield-efficiency",
        {"filters_applied", "data"},
    ),
    (
        "Crop seasonal trend",
        "/crops/seasonal-trend",
        {"filters_applied", "trend"},
    ),
    (
        "Market price comparison",
        "/markets/price-comparison?district=Chittagong",
        {"filters_applied", "comparison"},
    ),
    (
        "Crop quality breakdown",
        "/crops/quality-breakdown?crop_category=Vegetable&year=2023",
        {
            "filters_applied",
            "total_records",
            "grade_distribution",
            "pesticide_residue_breakdown",
        },
    ),
]


ERROR_CASES: list[tuple[str, str, int]] = [
    (
        "Invalid farm ID path validation",
        "/farms/999/performance",
        422,
    ),
    (
        "Invalid ranking metric validation",
        "/farms/top?metric=invalid_metric",
        422,
    ),
    (
        "Invalid quarter validation",
        "/crops/seasonal-trend?quarter=5",
        422,
    ),
    (
        "Invalid pesticide residue validation",
        "/crops/quality-breakdown?pesticide_residue=Extreme",
        422,
    ),
    (
        "No matching market price comparison rows",
        "/markets/price-comparison?crop_category=Cereal&year=2023&market_type=Export",
        404,
    ),
    (
        "No matching crop quality rows",
        "/crops/quality-breakdown?crop_id=999999",
        404,
    ),
]


def assert_success_case(title: str, path: str, required_keys: set[str]) -> None:
    response = client.get(path)

    if response.status_code != 200:
        raise AssertionError(
            f"{title} failed: expected 200, got {response.status_code}. "
            f"Response: {response.text}"
        )

    payload: dict[str, Any] = response.json()
    missing_keys = required_keys - set(payload.keys())

    if missing_keys:
        raise AssertionError(
            f"{title} failed: missing keys {sorted(missing_keys)}. "
            f"Payload keys: {sorted(payload.keys())}"
        )

    print(f"[PASS] {title}: 200 OK")


def assert_error_case(title: str, path: str, expected_status_code: int) -> None:
    response = client.get(path)

    if response.status_code != expected_status_code:
        raise AssertionError(
            f"{title} failed: expected {expected_status_code}, "
            f"got {response.status_code}. Response: {response.text}"
        )

    print(f"[PASS] {title}: {expected_status_code}")


def main() -> None:
    print("=" * 88)
    print("API SUCCESS CASES")
    print("=" * 88)

    for title, path, required_keys in SUCCESS_CASES:
        assert_success_case(title, path, required_keys)

    print()
    print("=" * 88)
    print("API ERROR CASES")
    print("=" * 88)

    for title, path, expected_status_code in ERROR_CASES:
        assert_error_case(title, path, expected_status_code)

    print()
    print("=" * 88)
    print("ALL API SMOKE CHECKS PASSED")
    print("=" * 88)


if __name__ == "__main__":
    main()