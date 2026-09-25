"""
task6.py

Reads task6_read_me.txt and counts the number of words in it.
"""

import os

# Resolve the path relative to this script's own directory so it works
# no matter what directory the script/tests are run from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# task6_read_me.txt lives at the project root (one level up from src/),
# not next to this script.
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_FILE_PATH = os.path.join(PROJECT_ROOT, "task6_read_me.txt")

def count_words_in_file(file_path):
    """
    Read the given text file and return the number of words in it.
    Words are determined by splitting on whitespace.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return len(content.split())


if __name__ == "__main__":
    word_count = count_words_in_file(DEFAULT_FILE_PATH)
    print(f"Word count in task6_read_me.txt: {word_count}")