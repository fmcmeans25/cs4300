"""
task3.py

Demonstrates three control structures:
1. if/elif/else  -> classify a number as positive, negative, or zero
2. for loop       -> find the first N prime numbers
3. while loop     -> sum all numbers from 1 to 100
"""


# ---------- 1. if statement ----------
def classify_number(n):
    """Return 'positive', 'negative', or 'zero' depending on n."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


# ---------- 2. for loop: prime numbers ----------
def is_prime(n):
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Only need to check odd divisors up to sqrt(n)
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def first_n_primes(count):
    """Return a list containing the first `count` prime numbers."""
    primes = []
    candidate = 2
    for _ in range(count):
        while not is_prime(candidate):
            candidate += 1
        primes.append(candidate)
        candidate += 1
    return primes


# ---------- 3. while loop: sum 1 to 100 ----------
def sum_1_to_100():
    """Return the sum of all integers from 1 to 100 using a while loop."""
    total = 0
    n = 1
    while n <= 100:
        total += n
        n += 1
    return total


if __name__ == "__main__":
    # 1. if statement demo
    for value in (5, -3, 0):
        print(f"{value} is {classify_number(value)}")

    # 2. for loop demo
    print("First 10 primes:", first_n_primes(10))

    # 3. while loop demo
    print("Sum of 1 to 100:", sum_1_to_100())