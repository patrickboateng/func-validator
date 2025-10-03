from typing import Annotated, Optional

import pytest

from func_validator import (
    validate_params,
    DependsOn,
    ValidationError,
)


def test_decorator():
    @validate_params
    def func(
            param1: str,
            param2: Annotated[Optional[str], DependsOn(param1="check")],
            # default strategy is value must not be empty.
    ):
        return param1, param2

    assert func("check", "value") == ("check", "value")

    with pytest.raises(ValidationError):
        func("check", "")
