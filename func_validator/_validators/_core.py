from typing import Callable, TypeAlias, TypeVar

Number: TypeAlias = int | float
T = TypeVar("T")


def _generic_number_validator(value: T, *, to: T, fn: Callable, symbol: str):
    if not fn(value, to):
        raise ValueError(f"Value {value} must be {symbol} {to}.")
