from collections import Counter

from advent.elf import read_lines


def part1(input):
    return sum(diff(s) for s in input)


HEX = "0123456789ABCDEFabcdef"


def diff(s):
    ans = 2
    i = 1
    while i < len(s) - 1:
        c = s[i]
        if c == '\\':
            n = s[i + 1]
            if n == '\\' or n == '"':
                ans += 1
                i += 1
            if n == 'x' and s[i + 2] in HEX and s[i + 3] in HEX:
                ans += 3
                i += 3
        i += 1
    return ans


def part2(input):
    return sum(increase(s) for s in input)


def increase(s):
    count = Counter(s)
    return 2 + count['"'] + count['\\']


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
