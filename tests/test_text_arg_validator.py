import re
from typing import Annotated

import pytest

from func_validator import (
    validate_func_args,
    MustMatchRegex,
    ValidationError,
    MustMatchBSCAddress,
    MustMatchEmail,
)


def test_must_match_regex_match():
    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(r"\d+")]):
        return x

    assert func("123") == "123"

    with pytest.raises(ValidationError):
        func("abc")


def test_must_match_regex_fullmatch():
    @validate_func_args
    def func(
        x: Annotated[str, MustMatchRegex(r"\d+", match_type="fullmatch")],
    ):
        return x

    assert func("456") == "456"

    with pytest.raises(ValidationError):
        func("456abc")


def test_must_match_regex_search():
    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(r"\d+", match_type="search")]):
        return x

    assert func("abc789xyz") == "abc789xyz"


def test_must_match_regex_with_flags():
    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(r"abc", flags=re.IGNORECASE)]):
        return x

    assert func("ABC") == "ABC"


def test_must_match_regex_type_error_non_string():
    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(r"\d+")]):
        return x

    with pytest.raises(TypeError):
        func(123)  # Passing an int should raise TypeError


def test_must_match_regex_error_message_contains_pattern():
    pattern = r"\d+"

    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(pattern)]):
        return x

    with pytest.raises(ValidationError):
        func("abc")


def test_must_match_regex_precompiled_pattern():
    compiled_pattern = re.compile(r"\d{3}")

    @validate_func_args
    def func(x: Annotated[str, MustMatchRegex(compiled_pattern)]):
        return x

    # Matching input should pass
    assert func("123") == "123"

    # Non-matching input should raise ValidationError
    with pytest.raises(ValidationError):
        func("12")


def test_must_match_regex_invalid_match_type():
    with pytest.raises(ValidationError):

        @validate_func_args
        def func(
            x: Annotated[
                str,
                MustMatchRegex(
                    r"abc", flags=re.IGNORECASE, match_type="invalid"
                ),
            ],
        ): ...


def test_must_match_bsc_address():
    @validate_func_args
    def func(address: Annotated[str, MustMatchBSCAddress]):
        return address

    assert func("0x4e5acf9684652BEa56F2f01b7101a225Ee33d23f")

    with pytest.raises(ValidationError):
        func("01234")


def test_must_match_email():
    @validate_func_args
    def func(email_addr: Annotated[str, MustMatchEmail]):
        return email_addr

    assert func("pato@gmail.com") == "pato@gmail.com"

    with pytest.raises(ValidationError):
        func("not-an-email")
