from typing import Annotated

import pytest

from func_validator import Validator, ValidationError, validate_params


def test_custom_validator():
    class MustBeEven(Validator):
        def __call__(self, arg_value, arg_name: str):
            if arg_value % 2 != 0:
                raise ValidationError(f"{arg_name}:{arg_value} must be even")

    @validate_params
    def func(even_num: Annotated[int, MustBeEven()]):
        return even_num

    assert func(4) == 4

    with pytest.raises(ValidationError):
        func(3)
