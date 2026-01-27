from typing import Annotated, Optional

import pytest

from func_validator import (
    DependsOn,
    MustBeMemberOf,
    MustBePositive,
    MustBeProvided,
    ValidationError,
    validate_params,
    MustBeLessThan,
)


class TestDependsOnValidator:
    @validate_params
    def decorated_fn(
        self,
        arg__1: Annotated[
            Optional[float],
            DependsOn(arg__2="rectangle", kw_strategy=MustBeProvided),
            MustBePositive(),
        ] = None,
        arg__2: Annotated[
            str, MustBeMemberOf(["square", "rectangle"])
        ] = "square",
    ):
        pass

    def test_depends_on_validator_4_kw_args(self):
        self.decorated_fn()
        self.decorated_fn(arg__1=10)
        self.decorated_fn(arg__1=10, arg__2="rectangle")

    def test_depends_on_validator_errors_4_kw_args(self):
        with pytest.raises(ValidationError):
            self.decorated_fn(arg__2="rectangle")

        with pytest.raises(ValidationError):
            self.decorated_fn(arg__1=-10)

    def test_depends_on_validator_4_pos_args(self):
        class A:

            def __init__(self, arg__1: int = 10, arg__2: int = 5):
                self.arg__1 = arg__1
                self.arg__2 = arg__2

            @property
            def arg__2(self):
                return self._arg__2

            @arg__2.setter
            @validate_params
            def arg__2(
                self,
                arg__2: Annotated[
                    int,
                    DependsOn("arg__1", args_strategy=MustBeLessThan),
                ],
            ):
                self._arg__2 = arg__2

        a = A()
        assert a.arg__2 == 5

        # If dependent argument does not exist.
        class B:

            def __init__(self, arg__1: int = 5):
                self.arg__1 = arg__1

            @property
            def arg__1(self):
                return self._arg__1

            @arg__1.setter
            @validate_params
            def arg__1(
                self,
                arg__1: Annotated[
                    int, DependsOn("arg__2", args_strategy=MustBeLessThan)
                ],
            ):
                self._arg__1 = arg__1

        with pytest.raises(ValidationError):
            B()
