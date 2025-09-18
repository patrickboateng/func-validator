from typing import TypeAlias, TypeVar

from validators.utils import ValidationError as Error

__all__ = ["Error", "Number", "OPERATOR_SYMBOLS", "T", "ValidationError"]

Number: TypeAlias = int | float
T = TypeVar("T")

OPERATOR_SYMBOLS: dict[str, str] = {
    "eq": "==",
    "ge": ">=",
    "gt": ">",
    "le": "<=",
    "lt": "<",
    "ne": "!=",
    "isclose": "≈",
}


class ValidationError(Exception):
    pass
