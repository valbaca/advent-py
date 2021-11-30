from advent.elf import read_lines, septoi

"""list.count is nice!"""


def main():
    part1(read_lines(__file__, septoi, True))
    part1(read_lines(__file__, septoi))
    part2(read_lines(__file__, septoi, True))
    part2(read_lines(__file__, septoi))


def part1(xs):
    n = 0
    for mn, mx, c, s in xs:
        if mn <= list(s).count(c) <= mx:
            n += 1
    print(n)


def part2(xs):
    n = 0
    for lo, hi, c, s in xs:
        cs = list(s)
        if (cs[lo - 1] == c) ^ (cs[hi - 1] == c):
            n += 1
    print(n)


if __name__ == '__main__':
    main()
