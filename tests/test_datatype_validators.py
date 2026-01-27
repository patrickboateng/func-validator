from typing import Annotated

import pytest

from func_validator import MustBeA, ValidationError, validate_params


def test_must_be_a_validator():
    @validate_params
    def fn(arg__1: Annotated[list, MustBeA(list)]):
        return arg__1

    assert fn([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        fn((1, 2, 3))

