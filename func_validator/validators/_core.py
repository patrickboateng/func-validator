from abc import ABC, abstractmethod
from string import Template
from typing import Optional, TypeAlias, TypeVar

__all__ = [
    "Number",
    "OPERATOR_SYMBOLS",
    "T",
    "ErrorMsg",
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


class ErrorMsg(Template):
    def transform(self, **kwargs):
        return self.safe_substitute(kwargs)


class Validator(ABC):

    def __init__(self, *, err_msg: str | ErrorMsg = "") -> None:
        if isinstance(err_msg, str):
            self.err_msg = ErrorMsg(err_msg)
        elif isinstance(err_msg, ErrorMsg):
            self.err_msg = err_msg
        else:
            raise ValidationError(
                f"err_msg must be str or ErrorMsg, not {type(err_msg)}"
            )

    @abstractmethod
    def __call__(self, *args, **kwargs) -> T: ...
