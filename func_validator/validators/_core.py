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
    def transform(self, **kwargs) -> str:
        return self.safe_substitute(kwargs)


class Validator(ABC):
    DEFAULT_ERROR_MSG: str

    def __init__(
        self,
        *,
        err_msg: str = "",
        extra_msg_args: Optional[dict] = None,
        default_err_msg: Optional[str] = None,
    ) -> None:
        self.err_msg = err_msg or default_err_msg
        self.extra_msg_args = extra_msg_args or {}

    @abstractmethod
    def __call__(self, *args, **kwargs) -> T: ...
