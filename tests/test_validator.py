import pytest
from func_validator import (
    MustBePositive, MustBeNonPositive, MustBeNonNegative, MustBeNegative,
    MustBeEqual, MustBeGreaterThan, MustBeLessThan, MustBeGreaterThanOrEqual,
    MustBeLessThanOrEqual, MustBeIn, MustBeBetween
)


# Numeric validation tests

@pytest.mark.parametrize("value", [1, 2.5, 100])
def test_MustBePositive(value):
    MustBePositive(value)


@pytest.mark.parametrize("value", [0, -1, -100])
def test_MustBeNonPositive(value):
    MustBeNonPositive(value)


@pytest.mark.parametrize("value", [0, 1, 2.5, 100])
def test_MustBeNonNegative(value):
    MustBeNonNegative(value)


@pytest.mark.parametrize("value", [-1, -2.5, -100])
def test_MustBeNegative(value):
    MustBeNegative(value)

# Comparison validation tests


# Membership and range validation tests
