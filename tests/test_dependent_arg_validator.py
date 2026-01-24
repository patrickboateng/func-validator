from typing import Annotated, Optional

import pytest

from func_validator import (
    DependsOn,
    MustBeMemberOf,
    MustBePositive,
    MustBeProvided,
    ValidationError,
    validate_params,
)


class TestDependsOnValidator:
    @validate_params
    def decorated_func(
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

    def test_depends_on_validator(self):
        self.decorated_func()
        self.decorated_func(arg__1=10)
        self.decorated_func(arg__1=10, arg__2="rectangle")

    def test_depends_on_validator_error(self):
        with pytest.raises(ValidationError):
            self.decorated_func(arg__2="rectangle")

        with pytest.raises(ValidationError):
            self.decorated_func(arg__1=-10)
