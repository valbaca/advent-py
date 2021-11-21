from collections import Counter

from advent.elf import lines, septoi


def part1(xs):
    n = 0
    for mn, mx, c, s in xs:
        counts = Counter(list(s))
        if mn <= counts[c] <= mx:
            n += 1
    print(n)


def part2(xs):
    n = 0
    for lo, hi, c, s in xs:
        cs = list(s)
        if (cs[lo-1] == c) ^ (cs[hi-1] == c):
            n += 1
    print(n)


if __name__ == '__main__':
    part1(lines(__file__, septoi, True))
    part1(lines(__file__, septoi))
    part2(lines(__file__, septoi, True))
    part2(lines(__file__, septoi))
