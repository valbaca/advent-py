from advent import elf


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


def parse(lines):
    return [elf.int_list(line) for line in lines]


def inc(grid, row, col):
    grid[row][col] += 1
    if grid[row][col] == 10:
        for [nrow, ncol] in elf.all_around(grid, row, col):
            inc(grid, nrow, ncol)


STEPS = 100


def part1(lines):
    grid = parse(lines)
    print(grid)
    total = 0
    for n in range(STEPS):
        for row, col in elf.iter_grid_indexes(grid):
            inc(grid, row, col)
        for row, col in elf.iter_grid_indexes(grid):
            if grid[row][col] > 9:
                total += 1
                grid[row][col] = 0

    return total


def part2(lines):
    grid = parse(lines)
    print(grid)
    octo_count = len(grid) * len(grid[0])
    n = 1
    while n > 0:
        for row, col in elf.iter_grid_indexes(grid):
            inc(grid, row, col)
        flashed = 0
        for row, col in elf.iter_grid_indexes(grid):
            if grid[row][col] > 9:
                flashed += 1
                grid[row][col] = 0
        if flashed == octo_count:
            return n
        n += 1
    return None


if __name__ == '__main__':
    main()
