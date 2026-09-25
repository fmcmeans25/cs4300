# CS4300 – Homework 1
 
A collection of small Python exercises (task1 through task7), each with
its own pytest test suite.
 
## Project structure
 
```
homework1/
├── src/
│   ├── task1.py    # prints "Hello, World!"
│   ├── task2.py    # data types demo (int, float, str, bool)
│   ├── task3.py    # if / for / while control structures, primes
│   ├── task4.py    # calculate_discount (duck typing)
│   ├── task5.py    # list slicing + dictionary (student database)
│   ├── task6.py    # reads task6_read_me.txt and counts words
│   └── task7.py    # numpy demo (array stats, normalization)
├── tests/
│   ├── task1_test.py
│   ├── task2_test.py
│   ├── task3_test.py
│   ├── task4_test.py
│   ├── task5_test.py
│   ├── task6_test.py
│   └── task7_test.py
├── task6_read_me.txt   # sample text read by task6.py
├── pytest.ini           # lets tests/ import modules from src/
├── run_tests.py          # master script: runs every test file at once
└── README.md
```
 
## Setup
 
From the `homework1/` directory:
 
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate          # Windows: venv\Scripts\activate
python3 -m pip install pytest numpy
```
 
(`numpy` is only needed for task7; the rest of the tasks use just the
standard library.)
 
## Running the tests
 
**Run everything at once** with the master runner:
 
```bash
python3 run_tests.py
```
 
Add flags as needed — they're passed straight through to pytest:
 
```bash
python3 run_tests.py -v          # verbose output
python3 run_tests.py -k task3    # run only task3's tests
```
 
**Run pytest directly** (equivalent, since `pytest.ini` points at
`tests/` and adds `src/` to the import path):
 
```bash
pytest
pytest tests/task3_test.py -v    # a single file
```
 
**Run a single task's script** directly:
 
```bash
python3 src/task1.py
```
 
## Notes
 
- Each `taskN_test.py` imports its corresponding module directly (e.g.
  `from task3 import classify_number`). This works without any
  `sys.path` hacking in the test files themselves because `pytest.ini`
  sets `pythonpath = src`, so `src/` is importable from anywhere tests
  are run.
- Verified against a full 7-task run: 52 tests collected, 52 passed.
- `task6.py` resolves the path to `task6_read_me.txt` relative to the
  project root (one level up from `src/`), so it works no matter which
  directory you run it from.