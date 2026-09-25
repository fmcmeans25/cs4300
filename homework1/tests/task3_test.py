"""
task3_test.py

Pytest test cases covering each control structure in task3.py.
"""

import pytest

from task3 import classify_number, is_prime, first_n_primes, sum_1_to_100


# ---------- 1. if statement tests ----------
def test_classify_positive():
    assert classify_number(5) == "positive"


def test_classify_negative():
    assert classify_number(-3) == "negative"


def test_classify_zero():
    assert classify_number(0) == "zero"


# ---------- 2. for loop / prime tests ----------
@pytest.mark.parametrize(
    "n, expected",
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (18, False),
    ],
)
def test_is_prime(n, expected):
    assert is_prime(n) == expected


def test_first_n_primes_returns_correct_list():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert first_n_primes(10) == expected


def test_first_n_primes_count():
    assert len(first_n_primes(10)) == 10


def test_first_n_primes_all_prime():
    assert all(is_prime(p) for p in first_n_primes(10))


# ---------- 3. while loop / sum tests ----------
def test_sum_1_to_100():
    assert sum_1_to_100() == 5050  # known closed-form result: n(n+1)/2 for n=100