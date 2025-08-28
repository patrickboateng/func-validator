from typing import Annotated

import pytest

from func_validator import MustBeA, validate_func_args, ValidationError


def test_must_be_a_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustBeA(list)]):
        return x_1

    assert func([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func((1, 2, 3))
