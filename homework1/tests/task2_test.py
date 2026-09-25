"""
test_test.py

Pytest test cases covering integer, float, string, and boolean behavior
in task2.py.
"""

import pytest

from task2 import add_integers, divide_floats, greet, is_even


# ---------- Integer tests ----------
def test_add_integers_returns_int():
    result = add_integers(2, 3)
    assert result == 5
    assert isinstance(result, int)


def test_add_integers_negative_numbers():
    assert add_integers(-4, -6) == -10


# ---------- Floating-point tests ----------
def test_divide_floats_returns_float():
    result = divide_floats(7.0, 2.0)
    assert result == pytest.approx(3.5)
    assert isinstance(result, float)


def test_divide_floats_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide_floats(1.0, 0.0)


# ---------- String tests ----------
def test_greet_returns_str():
    result = greet("World")
    assert result == "Hello, World!"
    assert isinstance(result, str)


def test_greet_with_empty_name():
    assert greet("") == "Hello, !"


# ---------- Boolean tests ----------
def test_is_even_true_case():
    result = is_even(4)
    assert result is True
    assert isinstance(result, bool)


def test_is_even_false_case():
    result = is_even(7)
    assert result is False
    assert isinstance(result, bool)