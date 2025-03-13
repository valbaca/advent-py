import bisect
import hashlib
import re
from functools import reduce
from math import inf
from typing import AnyStr, Pattern, List

"""
An elf is Santa's little helper, so elf.py has helper functions!
"""

N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
DIRS = [N, E, S, W]
def clockwise(dir, n=1):
    i = DIRS.index(dir)
    return DIRS[(i+n) % len(DIRS)]

def counterclockwise(dir, n=1):
    i = DIRS.index(dir)
    return DIRS[(i-n) % len(DIRS)]

# IO-related

def in_file(file):
    return file.replace(".py", ".txt")


def test_file(file):
    return file.replace(".py", "-test.txt")


def read_lines(filename: AnyStr, parser=None, test=False) -> List[str]:
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
    return blank_grouped(strip_lines(filename))


def blank_grouped(lines):
    groups = [[]]
    for line in lines:
        if line:
            groups[-1].append(line)
        else:
            groups.append([])  # blank line = new group
    return groups


# String related

def split_on(s: AnyStr, regex: Pattern[AnyStr] = r"[\W]") -> List[AnyStr]:
    """
    Like re.split, but also removes blanks.
    Default split regex is any non-alphanumeric (including hyphen! careful with negative numbers)
    """
    return [split for split in re.split(regex, s) if split]


def str_replace(s, pos, char):
    return s[:pos] + char + s[pos + 1:]


# String conversions

def safe_atoi(s: AnyStr):
    """Safe Ascii to Integer. If the string is an int, returns as an int; otherwise gives the string back"""
    out = s
    try:
        out = int(s)
    except (ValueError, TypeError):
        pass
    return out


def septoi(s: AnyStr, regex: Pattern[AnyStr] = r"[^a-zA-Z0-9-]") -> List[AnyStr]:
    """
    Separates string and applies safe_atoi
    :param s: string to be separated
    :param regex: regex to separate with. Default is split on non-alphanumeric-and-hyphen
    :return: separated parts as ints (where possible)
    """
    return list(map(safe_atoi, split_on(s, regex)))


def only_ints(xs: List):
    return [n for n in xs if isinstance(n, int)]


# Collections

def int_list(strs):
    return [int(s) for s in strs if s]


def bisect_index(arr, n):
    """
    Returns the index of n in the sorted list or None if n is not present in arr.
    """
    bi = bisect.bisect_left(arr, n)
    if bi < len(arr) and arr[bi] == n:
        return bi
    return None


# Grids / Matricies

def to_grid(lines):
    return [list(line) for line in lines]

def around_values(grid, r, c):
    """Return the values up/down/left/right; not diagonals"""
    return [grid[rd][cd] for rd, cd in around_indexes(grid, r, c)]


def around_indexes(grid, r, c):
    """Return the indicies up/down/left/right; not diagonals"""
    row = grid[r]
    diffs = [-1, 1]
    rows = [[r + d, c] for d in diffs if 0 <= r + d < len(grid)]
    cols = [[r, c + d] for d in diffs if 0 <= c + d < len(row)]
    return rows + cols


def diff3(val, lo=0, hi=inf, df=1):
    """Return list [val-df, val, val+df], clamped to [lo, hi)"""
    diffs = [val - df, val, val + df]
    return [x for x in diffs if lo <= x < hi]


def all_around(grid, row, col, df=1):
    """Return indexes of items around row, col in grid (including diagonals) but not grid[row][col] itself"""
    lst = []
    for nrow in diff3(row, hi=len(grid), df=df):
        for ncol in diff3(col, hi=len(grid[nrow]), df=df):
            if not (nrow == row and ncol == col):
                lst.append([nrow, ncol])
    return lst


def all_values_around(grid, row, col, df=1):
    """Return values of all items around row, col in grid (including diagonals) but not grid[row][col] itself"""
    return [grid[r][c] for r, c in all_around(grid, row, col, df)]


def enumerate_grid(grid):
    return [[rowi, row, coli, col] for rowi, row in enumerate(grid) for coli, col in enumerate(row)]


def iter_grid_values(grid):
    """Gives [row, col] value pairs for grid"""
    return [[row, col] for row in grid for col in row]


def iter_grid_indexes(grid):
    """Gives [rowi, coli] index pairs for grid"""
    return [[r, c] for r in range(len(grid)) for c in range(len(grid[r]))]

def iter_grid(grid):
    """Gives [rowi, coli, value] for grid"""
    return [[r,c,v] for r in range(len(grid)) for c, v in enumerate(grid[r])]


def transpose(m):
    """
    Transposes a matrix (a rectangle-shaped list of lists)
    If the input is a list of strings, the output is also a list of strings
    """
    rc = len(m)  # row count
    cc = len(m[0])  # col count
    if isinstance(m[0], str):
        return [''.join([m[r][c] for r in range(rc)]) for c in range(cc)]
    else:
        return [[m[r][c] for r in range(rc)] for c in range(cc)]


def get(g, rc, c=None):
    """
    Given a grid, row-column tuple OR grid, row, col...
    returns the value at the coordinates OR returns None if out of bounds
    """
    r = None
    if type(rc) is int:
        if c is None:
            raise TypeError("Expected c to be non-None if r is int")
        r = rc
    if type(rc) is tuple and c is None:
        r, c = rc
    if r is None:
        raise Exception("Expected r to be non-None if r is int")
    if 0 <= r < len(g) and 0 <= c < len(g[r]):
        return g[r][c]
    else:
        return None


# Math

def odd(n):
    return (n % 2) != 0


def even(n):
    return (n % 2) == 0


def product(xs):
    return reduce(lambda x, y: x * y, xs, 1)


def clamp(n, lo, hi):
    return max(lo, min(n, hi))


# Tuples...(though probably just use numpy?)

def mv(start, diff):
    return start[0] + diff[0], start[1] + diff[1]

def ad(a, b):
    """Add, for pair"""
    if type(b) is tuple or type(b) is list:
        return a[0] + b[0], a[1] + b[1]
    return a[0] + b, a[1] + b

def sb(a, b):
    """Subtract, for pair"""
    if type(b) is tuple or type(b) is list:
        return a[0] - b[0], a[1] - b[1]
    return a[0] - b, a[1] - b


def ml(a, b):
    """Multiply, for pair"""
    if type(b) is tuple or type(b) is list:
        return a[0] * b[0], a[1] * b[1]
    return a[0] * b, a[1] * b


def dv(a, b):
    """Divide, for pair"""
    if type(b) is tuple or type(b) is list:
        return a[0] // b[0], a[1] // b[1]
    return a[0] // b, a[1] // b


def md(a, b):
    """Mod % for pair"""
    if type(b) is tuple or type(b) is list:
        return a[0] % b[0], a[1] % b[1]
    return a[0] % b, a[1] % b


def dm(a, b):
    """divmod for pair"""
    if type(b) is tuple or type(b) is list:
        return divmod(a[0], b[0]), divmod(a[1], b[1])

    return divmod(a[0], b), divmod(a[1], b)


def is_even_div(a, b):
    """Return whether pair a is evenly/perfectly divisible by b, which can be a pair or scalar"""
    if type(b) is tuple or type(b) is list:
        dmx = divmod(a[0], b[0])  # div, mod
        return dmx[1] == 0 and dmx == divmod(a[1], b[1])
    else:
        dmx = divmod(a[0], b)
        return dmx[1] == 0 and dmx == divmod(a[1], b)


# Stealing from:
# https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset

def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def prefix_sums(xs):
    # then just use p[end] - p[start]
    pref_sums = [0] + xs[:]
    for i in range(1, len(pref_sums)):
        pref_sums[i] += pref_sums[i - 1]
    return pref_sums


def between(x, x1, x2):
    """Whether x is between (inclusive) x1 and x2.
    x1 and x2 can be in any order, allowing: between(0, 1, -1) == True
    If you want ordered, just use x1 <= x <= x2"""
    return x1 <= x <= x2 or x2 <= x <= x1


def md5(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def cmp(a, b):
    return (a > b) - (a < b)


# Numpy related

import numpy as np


def lines_to_np_array(lines):
    max_length = max(len(line) for line in lines)
    num_lines = len(lines)

    # Create a 2D NumPy array of characters filled with whitespace
    array = np.empty((num_lines, max_length), dtype=np.dtype('U1'))
    array.fill(' ')

    # Fill the array with characters from the text
    for i, line in enumerate(lines):
        array[i, :len(line)] = list(line)

    return array


# Algorithms

class Dijkstra:
    def __init__(self, grid):
        self.grid = grid

    def dijkstra(self, start):
        # start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [[inf] * len(self.grid) for _ in range(len(self.grid))]
        distances[start[0]][start[1]] = 0
        visited = [[False] * len(self.grid) for _ in range(len(self.grid))]

        for _, _ in iter_grid_indexes(self.grid):
            min_distance = inf

            u = None  # the node we inspect next...
            for r, c in iter_grid_indexes(self.grid):
                if not visited[r][c] and distances[r][c] < min_distance:
                    min_distance = distances[r][c]
                    u = r, c
            if u is None:
                break

            visited[u[0]][u[1]] = True

            for r, c in around_indexes(self.grid, u[0], u[1]):
                if self.grid[r][c] != '#' and not visited[r][c]:
                    alt = distances[u[0]][u[1]] + 1
                    if alt < distances[r][c]:
                        distances[r][c] = alt
        return distances
