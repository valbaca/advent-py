import bisect
import re
from functools import reduce
from typing import AnyStr, Pattern

"""
An elf is Santa's little helper, so elf.py has helper functions!
"""


# IO-related

def in_file(file):
    return file.replace(".py", ".txt")


def test_file(file):
    return file.replace(".py", "-test.txt")


def read_lines(filename: AnyStr, parser=None, test=False):
    """
    Returns the lines of input as a list of strings.
    If given a python file (preferred), like: lines(__file__)
    then the corresponding input is looked up (instead of the python source file)
    :param filename:
    :param parser: a function to apply to each line
    :param test: whether filename-test.txt should be used instead of filename.txt
    :return: lines of input as a list of strings
    """
    if filename.endswith(".py"):
        filename = test_file(filename) if test else in_file(filename)
    with open(filename, "r") as f:
        xs = [line.strip() for line in f.readlines() if line and line.strip()]
        if parser:
            xs = list(map(parser, xs))
        return xs


def strip_lines(filename):
    with open(filename) as f:
        arr = [line.strip() for line in f.readlines()]
    return arr


def lines_blank_grouped(filename):
    """For problems where the lines of input are grouped by blank lines."""
    orig_lines = strip_lines(filename)
    groups = [[]]
    for line in orig_lines:
        if line:
            groups[-1].append(line)
        else:
            groups.append([])  # blank line = new group
    return groups


# String related

def split_on(s: AnyStr, regex: Pattern[AnyStr] = r"[\W]") -> list[AnyStr]:
    """
    Like re.split, but also removes blanks.
    Default split regex is any non-alphanumeric (including hyphen! careful with negative numbers)
    """
    return [split for split in re.split(regex, s) if split]


# String conversions

def safe_atoi(s: AnyStr):
    """Safe Ascii to Integer. If the string is an int, returns as an int; otherwise gives the string back"""
    out = s
    try:
        out = int(s)
    except (ValueError, TypeError):
        pass
    return out


def septoi(s: AnyStr, regex: Pattern[AnyStr] = r"[^a-zA-Z0-9-]") -> list[AnyStr]:
    """
    Separates string and applies safe_atoi
    :param s: string to be separated
    :param regex: regex to separate with. Default is split on non-alphanumeric-and-hyphen
    :return: separated parts as ints (where possible)
    """
    return list(map(safe_atoi, split_on(s, regex)))


# Collections

def bisect_index(arr, n):
    """
    Returns the index of n in the sorted list or None if n is not present in arr.
    """
    bi = bisect.bisect_left(arr, n)
    if bi < len(arr) and arr[bi] == n:
        return bi
    return None


# Math

def odd(n):
    return (n % 2) != 0


def even(n):
    return (n % 2) == 0


def product(xs):
    return reduce(lambda x, y: x * y, xs, 1)
