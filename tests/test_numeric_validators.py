import pytest
from func_validator import (
    MustBePositive,
    MustBeNonPositive,
    MustBeNonNegative,
    MustBeNegative,
    MustBeEqual,
    MustBeGreaterThan,
    MustBeLessThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThanOrEqual,
)


# Numeric validation tests


def test_must_be_positive():
    MustBePositive(1)
    MustBePositive(2.5)

    with pytest.raises(ValueError):
        MustBePositive(0)


def test_must_be_non_positive():
    MustBeNonPositive(0)
    MustBeNonPositive(-1)
    MustBeNonPositive(-10)

    with pytest.raises(ValueError):
        MustBeNonPositive(10)


def test_must_be_non_negative():
    MustBeNonNegative(0)
    MustBeNonNegative(10)

    with pytest.raises(ValueError):
        MustBeNonNegative(-2.5)


def test_must_be_negative():
    MustBeNegative(-2.5)
    MustBeNegative(-10.0)

    with pytest.raises(ValueError):
        MustBeNegative(5.0)


# Comparison validation tests
def test_must_be_equal():
    validator = MustBeEqual(5)
    validator(5)
    with pytest.raises(ValueError):
        validator(4)


def test_must_be_greater_than():
    validator = MustBeGreaterThan(3)
    validator(4)
    with pytest.raises(ValueError):
        validator(2)


def test_must_be_less_than():
    validator = MustBeLessThan(10)
    validator(5)
    with pytest.raises(ValueError):
        validator(15)


def test_must_be_greater_than_or_equal():
    validator = MustBeGreaterThanOrEqual(5)
    validator(5)
    validator(6)
    with pytest.raises(ValueError):
        validator(4)


def test_must_be_less_than_or_equal():
    validator = MustBeLessThanOrEqual(5)
    validator(5)
    validator(4)
    with pytest.raises(ValueError):
        validator(6)
