from enum import Enum, IntEnum


class Region(str, Enum):
    DHAKA = "Dhaka"
    CHITTAGONG = "Chittagong"
    SYLHET = "Sylhet"
    RAJSHAHI = "Rajshahi"
    KHULNA = "Khulna"
    RANGPUR = "Rangpur"
    BARISAL = "Barisal"
    MYMENSINGH = "Mymensingh"


class FarmType(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    COMMERCIAL = "Commercial"


class CropCategory(str, Enum):
    CEREAL = "Cereal"
    VEGETABLE = "Vegetable"
    FRUIT = "Fruit"
    PULSE = "Pulse"
    OILSEED = "Oilseed"
    CASH_CROP = "Cash Crop"
    SPICE = "Spice"


class Season(str, Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"
    WINTER = "Winter"


class GrowingSeason(str, Enum):
    RABI = "Rabi"
    KHARIF = "Kharif"
    ZAID = "Zaid"
    YEAR_ROUND = "Year-Round"


class MarketType(str, Enum):
    LOCAL = "Local"
    WHOLESALE = "Wholesale"
    EXPORT = "Export"
    RETAIL = "Retail"
    GOVERNMENT_PROCUREMENT = "Government Procurement"


class PriceTier(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    PREMIUM = "Premium"


class QualityGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class PesticideResidue(str, Enum):
    NONE = "None"
    TRACE = "Trace"
    LOW = "Low"
    HIGH = "High"


class WaterRequirement(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Year(IntEnum):
    YEAR_2022 = 2022
    YEAR_2023 = 2023
    YEAR_2024 = 2024


class Quarter(IntEnum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4


class RankingMetric(str, Enum):
    PROFIT = "profit"
    REVENUE = "revenue"
    YIELD = "yield"