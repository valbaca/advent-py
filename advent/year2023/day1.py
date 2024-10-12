import math

from advent import elf

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    # print("Part 1 (test):")
    # print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    total = 0
    for line in lines:
        first, last = None, None
        for ch in line:
            if ch.isnumeric():
                if first is None:
                    first = ch
                last = ch
        total += int(first+last)
    return total

digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

def part2(lines):
    total = 0
    for line in lines:
        first, first_pos, last, last_pos = None, math.inf, None, math.inf
        for i, ch in enumerate(line):
            if ch.isnumeric():
                if first is None:
                    first = ch
                    first_pos = i
                last = ch
                last_pos = i
        # total += int(first + last)
        for str_dig, dig_val in digits.items():
            i = line.find(str_dig)
            if i == -1:
                continue
            if i < first_pos or first is None:
                first = dig_val
                first_pos = i
            if i > last_pos or last is None:
                last = dig_val
                last_pos = i
            i = line.rfind(str_dig)
            if i < first_pos:
                first = dig_val
                first_pos = i
            if i > last_pos:
                last = dig_val
                last_pos = i
        total += int(first + last)
    return total


if __name__ == '__main__':
    main()
