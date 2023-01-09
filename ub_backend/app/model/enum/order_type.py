from enum import Enum


class OrderType(str, Enum):
    deliver = "delivery"
    selftake = "selftake"
