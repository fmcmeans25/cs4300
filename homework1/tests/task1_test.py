"""
task1_test.py

Pytest test case that verifies task1.py's output by capturing stdout.
"""

from task1 import hello_world


def test_hello_world_output(capsys):
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"