"""
task4.py

Calculates the final price of a product after applying a discount
percentage. calculate_discount relies on duck typing: it doesn't check
whether `price` or `discount` are int or float specifically -- it just
uses them as numbers (arithmetic operators), so any numeric type that
supports subtraction, multiplication, and division works.
"""


def calculate_discount(price, discount):
    """
    Return the final price after applying a discount percentage.

    price:    the original price (any numeric type: int, float, etc.)
    discount: the discount percentage, e.g. 20 for 20% off
              (any numeric type: int, float, etc.)

    Because Python uses duck typing, this function doesn't care whether
    price/discount are int or float -- as long as they support the
    arithmetic operators used below, the calculation works.
    """
    final_price = price - (price * (discount / 100))
    return final_price


if __name__ == "__main__":
    print(calculate_discount(100, 20))       # ints
    print(calculate_discount(50.0, 10.0))    # floats
    print(calculate_discount(80, 12.5))      # mixed int/float