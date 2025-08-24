import re

import pytest

from func_validator import MustMatchRegex


def test_must_match_regex_with_string_pattern_match():
    validator = MustMatchRegex(r"\d{3}-\d{2}-\d{4}", match_type="match")
    validator("123-45-6789")
    with pytest.raises(ValueError):
        validator("abc-def-ghij")


def test_must_match_regex_with_string_pattern_fullmatch():
    validator = MustMatchRegex(r"\w+", match_type="fullmatch")
    validator("helloWorld")
    with pytest.raises(ValueError):
        validator("hello world")


def test_must_match_regex_with_string_pattern_search():
    validator = MustMatchRegex(r"world", match_type="search")
    validator("hello world")
    with pytest.raises(ValueError):
        validator("hello there")


def test_must_match_regex_with_compiled_pattern():
    pattern = re.compile(r"foo\d+")
    validator = MustMatchRegex(pattern)
    validator("foo123")
    with pytest.raises(ValueError):
        validator("bar123")


def test_must_match_regex_with_flags():
    validator = MustMatchRegex(r"abc", match_type="match", flags=re.IGNORECASE)
    validator("ABC")
    with pytest.raises(ValueError):
        validator("def")


def test_must_match_regex_invalid_match_type():
    with pytest.raises(ValueError):
        MustMatchRegex(r".*", match_type="invalid")
