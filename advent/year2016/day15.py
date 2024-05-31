from itertools import count

from advent import elf


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def is_open(positions, start, time):
    return (start + time) % positions == 0


def runner(discs):
    for t in count(start=0):
        if all(is_open(pos, start, t + i + 1) for i, (pos, start) in enumerate(discs)):
            return t


def parse_discs(lines):
    discs = []
    for line in lines:
        _, positions, _, start_pos = elf.only_ints([elf.safe_atoi(s) for s in elf.split_on(line)])
        discs.append((positions, start_pos))
    return discs


def part1(lines):
    return runner(parse_discs(lines))


def part2(lines):
    return runner([*parse_discs(lines), (11, 0)])


if __name__ == '__main__':
    main()
