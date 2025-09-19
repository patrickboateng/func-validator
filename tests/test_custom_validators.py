import pytest
from func_validator import ValidationError, validate_func_args
from typing import Iterable, Annotated

from func_validator import validator


def test_custom_validator():
    @validator
    def must_be_even(arg_val: int, arg_name: str) -> tuple[bool, str]:
        check = arg_val % 2 == 0
        if check:
            return check, ""

        return check, f"{arg_name}:{arg_val} must be even"

    @validate_func_args
    def func(even_num: Annotated[int, must_be_even]):
        return even_num

    assert func(4) == 4

    with pytest.raises(ValidationError):
        func(3)
