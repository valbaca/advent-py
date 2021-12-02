from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2 (test):", part2(test_lines))

    print("Part 2:", part2(lines))


def part1(lines):
    depth = 0
    horz = 0
    for line in lines:
        op, arg = line.split(" ")
        arg = elf.safe_atoi(arg)
        if op == 'forward':
            horz += arg
        elif op == 'down':
            depth += arg
        elif op == 'up':
            depth -= arg
    return depth * horz


def part2(lines):
    depth = 0
    horz = 0
    aim = 0
    for line in lines:
        op, arg = line.split(" ")
        arg = elf.safe_atoi(arg)
        if op == 'forward':
            horz += arg
            depth += (aim * arg)
        elif op == 'down':
            aim += arg
        elif op == 'up':
            aim -= arg
    return depth * horz


if __name__ == '__main__':
    main()
