"""
task7.py

Demonstrates the numpy package (installed via `pip install numpy`).
numpy is a numerical computing library that provides fast array
operations. This script builds a small dataset of student test scores
and uses numpy to compute basic statistics on it.
"""

import numpy as np


def create_scores_array(scores):
    """Convert a list of numbers into a numpy array."""
    return np.array(scores)


def compute_statistics(scores):
    """
    Given a list (or numpy array) of numeric scores, return a dictionary
    of basic statistics computed using numpy: mean, median, std (standard
    deviation), min, and max.
    """
    arr = np.array(scores)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def normalize_scores(scores):
    """
    Scale scores to a 0-1 range using min-max normalization:
    (x - min) / (max - min)
    Returns a numpy array of normalized values.
    """
    arr = np.array(scores, dtype=float)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val == min_val:
        # Avoid division by zero when all scores are identical
        return np.zeros_like(arr)
    return (arr - min_val) / (max_val - min_val)


if __name__ == "__main__":
    test_scores = [72, 85, 90, 66, 95, 78, 88]

    arr = create_scores_array(test_scores)
    print("Scores array:", arr)

    stats = compute_statistics(test_scores)
    print("Statistics:", stats)

    normalized = normalize_scores(test_scores)
    print("Normalized scores:", normalized)