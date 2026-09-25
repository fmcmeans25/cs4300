"""
task5.py

Demonstrates two core data structures:
1. A list of favorite books (title, author) tuples, with list slicing
   to grab the first three.
2. A dictionary representing a basic student database (name -> ID).
"""


# ---------- List: favorite books ----------
def get_favorite_books():
    """Return a list of (title, author) tuples."""
    return [
        ("Dune", "Frank Herbert"),
        ("1984", "George Orwell"),
        ("The Hobbit", "J.R.R. Tolkien"),
        ("Brave New World", "Aldous Huxley"),
        ("Fahrenheit 451", "Ray Bradbury"),
    ]


def first_three_books(books):
    """Use list slicing to return the first three books in the list."""
    return books[:3]


# ---------- Dictionary: student database ----------
def get_student_database():
    """Return a dictionary mapping student names to student IDs."""
    return {
        "Alice Johnson": "S1001",
        "Bob Smith": "S1002",
        "Carla Diaz": "S1003",
        "David Lee": "S1004",
    }


def get_student_id(database, name):
    """Look up a student's ID by name. Returns None if not found."""
    return database.get(name)


if __name__ == "__main__":
    books = get_favorite_books()
    print("All favorite books:")
    for title, author in books:
        print(f"  {title} by {author}")

    print("\nFirst three books (via slicing):")
    for title, author in first_three_books(books):
        print(f"  {title} by {author}")

    students = get_student_database()
    print("\nStudent database:")
    for name, student_id in students.items():
        print(f"  {name}: {student_id}")

    print("\nLookup 'Bob Smith':", get_student_id(students, "Bob Smith"))