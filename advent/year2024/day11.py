from functools import cache

from advent import elf
from advent.elf import even


# FIBONACCI!!!!!!!!!!!!!!!!
# Love how easy Python makes this with @cache

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


def stone(s):
    if s == 0:
        return [1]
    else:
        st = str(s)
        if even(len(st)):
            return [int(st[:len(st) // 2]), int(st[len(st) // 2:])]
        else:
            return [2024 * s]


@cache
def stone_times(s, n):
    if n == 0:
        return 1
    ns = stone(s)
    if n == 1:
        return len(ns)
    return sum(stone_times(sub_s, n - 1) for sub_s in ns)


def part1(lines):
    stones = elf.septoi(lines[0])
    return sum(stone_times(s, 25) for s in stones)


def part2(lines):
    stones = elf.septoi(lines[0])
    return sum(stone_times(s, 75) for s in stones)


if __name__ == '__main__':
    main()
