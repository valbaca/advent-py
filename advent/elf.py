import re
from typing import AnyStr, Pattern


def howdy():
    print("Howdy!")


def _in_file(file):
    return file.replace(".py", ".txt")


def _test_file(file):
    return file.replace(".py", "-test.txt")


def lines(filename: AnyStr, parser=None, test=False):
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
        filename = _test_file(filename) if test else _in_file(filename)
    with open(filename, "r") as f:
        xs = [line for line in f.readlines() if line]
        if parser:
            xs = list(map(parser, xs))
        return xs


def split_on(s: AnyStr, regex: Pattern[AnyStr] = r"[\W]") -> list[AnyStr]:
    """
    Like re.split, but also removes blanks.
    Default split regex is any non-alphanumeric (including hyphen! careful with negative numbers)
    """
    return [split for split in re.split(regex, s) if split]


def safe_atoi(s: AnyStr):
    """Safe Ascii to Integer. If the string is an int, returns as an int; otherwise gives the string back"""
    out = s
    try:
        out = int(s)
    except (ValueError, TypeError):
        pass
    return out


def septoi(s: AnyStr, regex: Pattern[AnyStr] = r"[\W]") -> list[AnyStr]:
    """
    Separates string and applies safe_atoi
    :param s: string to be separated
    :param regex: regex to separate with. Default is split on non-alphanumeric
    :return: separated parts as ints (where possible)
    """
    return list(map(safe_atoi, split_on(s, regex)))
