from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, TypeAlias, TypeVar

__all__ = [
    "Number",
    "OPERATOR_SYMBOLS",
    "T",
    "Validator",
    "ValidationError",
]

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


class Validator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> T: ...


# def validator(func: Callable[[T, str], tuple[bool, str]]):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result, msg = func(*args, **kwargs)
#         if not result:
#             raise ValidationError(msg)
#
#     return wrapper
