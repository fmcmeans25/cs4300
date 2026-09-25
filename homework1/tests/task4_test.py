"""
task4_test.py

Pytest test cases for calculate_discount, covering integers, floats,
and mixed-type inputs to demonstrate duck typing in action.
"""

import pytest

from task4 import calculate_discount


def test_calculate_discount_with_integers():
    # 100 - (100 * 20/100) = 80
    assert calculate_discount(100, 20) == 80


def test_calculate_discount_with_floats():
    # 50.0 - (50.0 * 10.0/100) = 45.0
    result = calculate_discount(50.0, 10.0)
    assert result == pytest.approx(45.0)


def test_calculate_discount_with_mixed_types():
    # int price, float discount: 80 - (80 * 12.5/100) = 70.0
    result = calculate_discount(80, 12.5)
    assert result == pytest.approx(70.0)


def test_calculate_discount_zero_discount():
    # No discount should return the original price unchanged
    assert calculate_discount(100, 0) == 100


def test_calculate_discount_full_discount():
    # 100% discount should reduce price to 0
    assert calculate_discount(100, 100) == 0


def test_calculate_discount_returns_numeric_type():
    result = calculate_discount(100, 20)
    # Duck typing: we only care that it behaves like a number,
    # not that it's a specific type.
    assert result + 0 == result  # supports arithmetic like a number