from advent import elf
from collections import Counter


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))

    print("Part 2 (test):", part2(test_lines))
    print("Part 2:", part2(lines))

def count_line_chars(lines):
    line_len = len(lines[0])
    counts = [Counter() for _ in range(line_len)]
    for line in lines:
        for i, ch in enumerate(line):
            counts[i][ch] += 1
    return counts


def part1(lines):
    return ''.join((count.most_common()[0][0] for count in count_line_chars(lines)))



def part2(lines):
    return ''.join((count.most_common()[-1][0] for count in count_line_chars(lines)))


if __name__ == '__main__':
    main()
