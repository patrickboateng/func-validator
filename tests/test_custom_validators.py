from typing import Annotated

import pytest

from func_validator import ValidationError, Validator, validate_params


def test_custom_validator():
    class MustBeEven(Validator):
        def __call__(self, arg_value, arg_name: str):
            if arg_value % 2 != 0:
                raise ValidationError(f"{arg_name}:{arg_value} must be even")

    @validate_params
    def fn(arg__1: Annotated[int, MustBeEven()]):
        return arg__1

    assert fn(4) == 4

    with pytest.raises(ValidationError):
        fn(3)
