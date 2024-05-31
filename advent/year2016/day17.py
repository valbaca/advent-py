from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def part1(lines):
    ...


def part2(lines):
    ...


if __name__ == '__main__':
    main()
