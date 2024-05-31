from more_itertools import chunked


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))
    #
    # lines = elf.read_lines(__file__)
    print("Part 1:", part1())
    print("Part 2:", part2())


def dragon(input, length):
    s = input
    while len(s) < length:
        a = s
        b = reversed(s)
        b = "".join(['0' if c == '1' else '1' for c in b])
        s = f"{a}0{b}"
    return s[:length]


def checksum(s):
    sm = ""
    while not sm or len(s) % 2 == 0:
        sm = "".join('1' if a == b else '0' for a, b in chunked(s, 2))
        s = sm
    return sm


def part1():
    return checksum(dragon('10111100110001111', 272))


def part2():
    return checksum(dragon('10111100110001111', 35651584))


if __name__ == '__main__':
    main()
