"""
task6_test.py

Pytest test cases that verify count_words_in_file works correctly,
both on the provided task6_read_me.txt and on temporary text files
created during the test run.
"""

import os

from task6 import count_words_in_file, DEFAULT_FILE_PATH


def test_word_count_in_task6_read_me():
    # The lorem ipsum passage in task6_read_me.txt contains 104 words.
    assert count_words_in_file(DEFAULT_FILE_PATH) == 104


def test_word_count_file_exists():
    assert os.path.isfile(DEFAULT_FILE_PATH)


def test_word_count_simple_sentence(tmp_path):
    file_path = tmp_path / "simple.txt"
    file_path.write_text("The quick brown fox jumps over the lazy dog")
    assert count_words_in_file(str(file_path)) == 9


def test_word_count_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")
    assert count_words_in_file(str(file_path)) == 0


def test_word_count_multiple_lines_and_spacing(tmp_path):
    file_path = tmp_path / "multiline.txt"
    file_path.write_text("Hello   world\n\nThis is   a test.\n")
    # "Hello", "world", "This", "is", "a", "test." -> 6 words
    assert count_words_in_file(str(file_path)) == 6