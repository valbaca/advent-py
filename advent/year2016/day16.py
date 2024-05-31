import time

from more_itertools import chunked


def main():
    print("Part 1:", part1())
    start = time.time()
    print("Part 2:", part2())
    end = time.time()
    print(f"{end - start:.2f}s")


def dragon(s, length):
    while len(s) < length:
        b = "".join([{'0': '1', '1': '0'}[c] for c in s[::-1]])
        s = f"{s}0{b}"
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
