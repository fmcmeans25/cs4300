"""
task2.py

Demonstrates basic Python data types (int, float, str, bool) through
simple functions, each of which performs a small, predictable operation
so its behavior can be verified with pytest.
"""


# ---------- Integer ----------
def add_integers(a: int, b: int) -> int:
    """Add two integers and return an integer result."""
    return a + b


# ---------- Floating-point ----------
def divide_floats(a: float, b: float) -> float:
    """Divide two floats and return a float result."""
    return a / b


# ---------- String ----------
def greet(name: str) -> str:
    """Return a greeting string built from the given name."""
    return f"Hello, {name}!"


# ---------- Boolean ----------
def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


if __name__ == "__main__":
    print(add_integers(2, 3))
    print(divide_floats(7.0, 2.0))
    print(greet("World"))
    print(is_even(4))