"""
task5_test.py

Pytest test cases covering the list (favorite books) and dictionary
(student database) data structures in task5.py.
"""

from task5 import (
    get_favorite_books,
    first_three_books,
    get_student_database,
    get_student_id,
)


# ---------- List tests ----------
def test_get_favorite_books_is_list_of_tuples():
    books = get_favorite_books()
    assert isinstance(books, list)
    assert len(books) >= 3
    for entry in books:
        assert isinstance(entry, tuple)
        assert len(entry) == 2  # (title, author)


def test_first_three_books_returns_three_items():
    books = get_favorite_books()
    result = first_three_books(books)
    assert len(result) == 3


def test_first_three_books_matches_slice():
    books = get_favorite_books()
    result = first_three_books(books)
    assert result == books[0:3]


def test_first_three_books_content():
    books = get_favorite_books()
    result = first_three_books(books)
    assert result[0] == ("Dune", "Frank Herbert")
    assert result[1] == ("1984", "George Orwell")
    assert result[2] == ("The Hobbit", "J.R.R. Tolkien")


# ---------- Dictionary tests ----------
def test_get_student_database_is_dict():
    students = get_student_database()
    assert isinstance(students, dict)
    assert len(students) >= 3


def test_get_student_id_found():
    students = get_student_database()
    assert get_student_id(students, "Bob Smith") == "S1002"


def test_get_student_id_not_found():
    students = get_student_database()
    assert get_student_id(students, "Nonexistent Student") is None


def test_student_ids_are_unique():
    students = get_student_database()
    ids = list(students.values())
    assert len(ids) == len(set(ids))