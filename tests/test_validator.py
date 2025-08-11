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
    MustBeIn,
    MustBeBetween,
    MustBeNonEmpty,
)


# Numeric validation tests


def test_MustBePositive():
    MustBePositive(1)
    MustBePositive(2.5)

    with pytest.raises(ValueError):
        MustBePositive(0)


def test_MustBeNonPositive():
    MustBeNonPositive(0)
    MustBeNonPositive(-1)
    MustBeNonPositive(-10)

    with pytest.raises(ValueError):
        MustBeNonPositive(10)


def test_MustBeNonNegative():
    MustBeNonNegative(0)
    MustBeNonNegative(10)

    with pytest.raises(ValueError):
        MustBeNonNegative(-2.5)


def test_MustBeNegative():
    MustBeNegative(-2.5)
    MustBeNegative(-10.0)

    with pytest.raises(ValueError):
        MustBeNegative(5.0)


# Comparison validation tests
def test_MustBeEqual():
    validator = MustBeEqual(5)
    validator(5)
    with pytest.raises(ValueError):
        validator(4)


def test_MustBeGreaterThan():
    validator = MustBeGreaterThan(3)
    validator(4)
    with pytest.raises(ValueError):
        validator(2)


def test_MustBeLessThan():
    validator = MustBeLessThan(10)
    validator(5)
    with pytest.raises(ValueError):
        validator(15)


def test_MustBeGreaterThanOrEqual():
    validator = MustBeGreaterThanOrEqual(5)
    validator(5)
    validator(6)
    with pytest.raises(ValueError):
        validator(4)


def test_MustBeLessThanOrEqual():
    validator = MustBeLessThanOrEqual(5)
    validator(5)
    validator(4)
    with pytest.raises(ValueError):
        validator(6)


# Membership and range validation tests


def test_MustBeIn():
    validator = MustBeIn([1, 2, 3])
    validator(2)
    with pytest.raises(ValueError):
        validator(4)


def test_MustBeBetween():
    validator = MustBeBetween(min_value=1, max_value=5)
    validator(1)
    validator(3)
    validator(5)
    with pytest.raises(ValueError):
        validator(0)
    with pytest.raises(ValueError):
        validator(6)


def test_MustBeNonEmpty():
    MustBeNonEmpty("a")
    MustBeNonEmpty([1])
    with pytest.raises(ValueError):
        MustBeNonEmpty("")
    with pytest.raises(ValueError):
        MustBeNonEmpty([])
