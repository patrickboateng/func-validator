from functools import wraps
from typing import TypeAlias, TypeVar, Callable

# ValidationError from python-validators package
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


def validator(func: Callable[[T, str], tuple[bool, str]]):
    @wraps(func)
    def wrapper(arg_val: T, arg_name: str):
        result, msg = func(arg_val, arg_name)
        if not result:
            raise ValidationError(msg)

    return wrapper
