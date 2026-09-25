"""
run_tests.py

Master test runner for the CS4300 homework1 project.

Discovers and runs every pytest test file under tests/ (task1_test.py
through task7_test.py, and any others added later), then prints a
pass/fail summary.

Usage:
    python3 run_tests.py            # run everything, normal output
    python3 run_tests.py -v         # run everything, verbose output
    python3 run_tests.py -k task3   # run only tests matching "task3"

Any extra command-line arguments are passed straight through to pytest,
so standard pytest flags work here too.
"""

import sys
import pytest


def main():
    # Extra args typed after run_tests.py (e.g. -v, -k task3) are
    # forwarded to pytest as-is.
    extra_args = sys.argv[1:]

    args = ["tests"] + extra_args

    print("=" * 60)
    print("Running all tests in tests/ ...")
    print("=" * 60)

    exit_code = pytest.main(args)

    print("=" * 60)
    if exit_code == 0:
        print("All tests passed!")
    else:
        print("Some tests failed. See output above for details.")
    print("=" * 60)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()