import string
from collections import defaultdict

from advent import elf


# TIL: using id() to avoid adding the same number twice to a list
# not even sure I needed it but nice to know python easily handles this

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def adjacent(grid, r, cs):  # rows, columns
    for c in cs:
        symbols = [v for v in elf.all_values_around(grid, r, c) if (v != '.') and (not v.isdigit())]
        if len(symbols) > 0:
            return True
    return False


def part1(lines):
    grid = [list(line) for line in lines]

    score = 0
    for r, row in enumerate(grid):
        num_str = ""
        num_pos = []  # column of the chars
        for c, ch in enumerate(row):
            if ch.isdigit():
                num_str += ch
                num_pos.append(c)
            if num_str and (not ch.isdigit() or c == len(row) - 1):
                if adjacent(grid, r, num_pos):
                    score += int(num_str)
                # reset
                num_str = ""
                num_pos = []  # column of the chars
    return score


def update_gears(grid, r, cs, gears, num_val):
    for c in cs:
        idxs = elf.all_around(grid, r, c)
        for ir, ic in idxs:
            if grid[ir][ic] == '*':
                gear_key = f"{ir},{ic}"
                gear_vals = gears[gear_key]
                # using id() to ensure we're not adding the *same* number twice!
                if any(id(num_val) == id(gear_val) for gear_val in gear_vals):
                    continue
                else:
                    gears[gear_key].append(num_val)

    for c in cs:
        symbols = [v for v in elf.all_values_around(grid, r, c) if (v != '.') and (not v.isdigit())]
        if len(symbols) > 0:
            return True
    return False


def part2(lines):
    grid = [list(line) for line in lines]
    gears = defaultdict(list)  # gear "r,c": [nums]
    for r, row in enumerate(grid):
        num_str = ""
        num_pos = []  # column of the chars
        for c, ch in enumerate(row):
            if ch.isdigit():
                num_str += ch
                num_pos.append(c)
            if num_str and (not ch.isdigit() or c == len(row) - 1):
                update_gears(grid, r, num_pos, gears, int(num_str))
                # reset
                num_str = ""
                num_pos = []  # column of the chars
    return sum(
        gv[0] * gv[1] for gv in gears.values() if len(gv) == 2
    )


if __name__ == '__main__':
    main()
