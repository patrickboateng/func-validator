from typing import Annotated, Optional

import pytest

from func_validator import (
    validate_params,
    DependsOn,
    ValidationError,
    MustBeLessThan,
)


def test_decorator():
    @validate_params
    def func(
        param1: str,
        param2: Annotated[Optional[str], DependsOn(param1="check")],
        # default strategy is value must not be empty.
    ) -> tuple:
        return param1, param2

    assert func("check", "value") == ("check", "value")
    assert func("check2", "value") == ("check2", "value")

    with pytest.raises(ValidationError):
        func("check", "")

    with pytest.raises(TypeError):
        validate_params("t")

    class A:

        def __init__(self, age: int = 10, height: int = 5):
            self.age = age
            self.height = height

        @property
        def height(self):
            return self._height

        @height.setter
        @validate_params
        def height(
            self,
            height: Annotated[
                int, DependsOn("age", args_strategy=MustBeLessThan)
            ],
        ):
            self._height = height

    a = A()
    assert a.height == 5

    class B:

        def __init__(self, weight: int = 5):
            self.weight = weight

        @property
        def weight(self):
            return self._weight

        @weight.setter
        @validate_params
        def weight(
            self,
            weight: Annotated[
                int, DependsOn("age", args_strategy=MustBeLessThan)
            ],
        ):
            self._weight = weight

    with pytest.raises(ValidationError):
        B()
