"""
task7_test.py

Pytest test cases verifying the correctness of the numpy-based
functions in task7.py.
"""

import numpy as np
import pytest

from task7 import create_scores_array, compute_statistics, normalize_scores


# ---------- create_scores_array ----------
def test_create_scores_array_returns_ndarray():
    result = create_scores_array([1, 2, 3])
    assert isinstance(result, np.ndarray)


def test_create_scores_array_values():
    result = create_scores_array([1, 2, 3])
    assert list(result) == [1, 2, 3]


# ---------- compute_statistics ----------
def test_compute_statistics_mean():
    stats = compute_statistics([10, 20, 30])
    assert stats["mean"] == pytest.approx(20.0)


def test_compute_statistics_median():
    stats = compute_statistics([10, 20, 30])
    assert stats["median"] == pytest.approx(20.0)


def test_compute_statistics_min_max():
    stats = compute_statistics([72, 85, 90, 66, 95, 78, 88])
    assert stats["min"] == 66.0
    assert stats["max"] == 95.0


def test_compute_statistics_std():
    # Standard deviation of [2, 4, 4, 4, 5, 5, 7, 9] is 2.0 (population std)
    stats = compute_statistics([2, 4, 4, 4, 5, 5, 7, 9])
    assert stats["std"] == pytest.approx(2.0)


def test_compute_statistics_returns_dict_with_expected_keys():
    stats = compute_statistics([1, 2, 3])
    assert set(stats.keys()) == {"mean", "median", "std", "min", "max"}


# ---------- normalize_scores ----------
def test_normalize_scores_range_is_0_to_1():
    result = normalize_scores([66, 72, 78, 85, 88, 90, 95])
    assert result.min() == pytest.approx(0.0)
    assert result.max() == pytest.approx(1.0)


def test_normalize_scores_known_values():
    # For [0, 5, 10]: normalized -> [0.0, 0.5, 1.0]
    result = normalize_scores([0, 5, 10])
    np.testing.assert_allclose(result, [0.0, 0.5, 1.0])


def test_normalize_scores_identical_values():
    # All identical values should normalize to all zeros (no division by zero)
    result = normalize_scores([7, 7, 7])
    np.testing.assert_allclose(result, [0.0, 0.0, 0.0])