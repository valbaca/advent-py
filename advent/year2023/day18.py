from itertools import pairwise

from advent import elf
from advent.elf import mv


"""
TIL: Shoelace and Pick's Theorem

I'd skipped these when I did Day 10, but figured it was time to actually hold my nose and learn!

HUGE thanks to xavdid: https://advent-of-code.xavd.id/writeups/2023/day/18/
- Shoelace Thorem: https://www.youtube.com/watch?v=65ATI8PqIts
- Proving Pick's Theorem: https://www.youtube.com/watch?v=bYW1zOMCQno
"""

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


DIRS = {'U': (-1, 0), 'L': (0, -1), 'R': (0, 1), 'D': (1, 0)}


def count_fill(points, length=None):
    """Given a list of points, returns the area 'filled' by those points"""
    if length is None:
        length = len(points)  # for part 2
    # shoelace - find the area of a shape
    area = sum(a[0] * b[1] - a[1] * b[0] for a, b in pairwise(points)) // 2
    # pick's theorem
    return int(abs(area) - (length // 2)) + length


def part1(lines):
    grid = [(0, 0)]

    for line in lines:
        d, n_str, _ = elf.split_on(line, r"\s")
        for _ in range(int(n_str)):
            grid.append(mv(grid[-1], DIRS[d]))
    return count_fill(grid)


def part2(lines):
    grid = [(0, 0)]
    full_len = 1

    for line in lines:
        _, _, hex_str = elf.split_on(line, r"\s")
        n = int(hex_str[2:-2], base=16)
        d = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[hex_str[-2:-1]]
        grid.append(mv(grid[-1], (DIRS[d][0] * n, DIRS[d][1] * n)))
        full_len += n
    return count_fill(grid, full_len)


if __name__ == '__main__':
    main()
