"""Smoke tests: run every .sm example + Phase 1 checks. Exit nonzero on failure."""
import io
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang.parser import parse
from lang.interp import run


def run_sm(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    buf = io.StringIO()
    run(parse(src), out=buf)
    return buf.getvalue().splitlines()


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ex = lambda n: os.path.join(root, "examples", n)

lines = run_sm(ex("hello.sm"))
assert lines[0] == "hello world", lines[0]
assert lines[1] == "hi sami", lines[1]
assert lines[2] == "15" and lines[3] == "17", lines[2:4]
assert lines[4] == "big", lines[4]
assert lines[5:10] == ["0", "1", "4", "9", "16"], lines[5:10]
assert lines[10:13] == ["0", "1", "2"], lines[10:13]
assert lines[13] == "610", lines[13]

lines = run_sm(ex("fizzbuzz.sm"))
assert lines[2] == "Fizz" and lines[4] == "Buzz" and lines[14] == "FizzBuzz", lines

lines = run_sm(ex("primes.sm"))
assert lines == ["2", "3", "5", "7", "11", "13", "17", "19", "23", "29"], lines

lines = run_sm(ex("collatz.sm"))
assert lines[0] == "27" and lines[-3] == "1", lines[:2]
assert lines[-2:] == ["steps:", "111"], lines[-2:]

from myai.phase1 import check  # noqa: runs asserts on import

print("smoke OK: 4 programs + phase 1")
