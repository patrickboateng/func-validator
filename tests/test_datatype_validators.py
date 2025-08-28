from typing import Annotated, Optional

import pytest

from func_validator import MustBeA, validate_func_args, ValidationError


def test_must_be_a_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustBeA(list)]):
        return x_1

    assert func([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func((1, 2, 3))

    @validate_func_args(check_arg_types=True)
    def func_2(x_1: Annotated[Optional[int], MustBeA(int)]):
        return x_1

    assert func_2(2) == 2
    assert func_2(None) is None

    with pytest.raises(TypeError):
        func_2((1, 2, 3))

    with pytest.raises(TypeError):
        validate_func_args("invalid")

    @validate_func_args
    def func_3(x_1: int, x_2: Annotated[int, "Just a Metadata"]):
        return x_1, x_2

    assert func_3(2, 3) == (2, 3)
