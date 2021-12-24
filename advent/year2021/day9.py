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


def part1(lines):
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])
    risk = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            this = grid[r][c]
            ars = elf.arounds(grid, r, c)
            if all([this < x for x in ars]):
                risk += this + 1

    return risk


def part2(lines):
    grid = []
    basin = []
    for line in lines:
        grid.append([int(c) for c in line])
        basin.append([None] * len(line))
    basin_bottoms = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            this = grid[r][c]
            ars = elf.arounds(grid, r, c)
            if all([this < x for x in ars]):
                basin_bottoms.append([r, c])
    for r, c in basin_bottoms:
        find_basin(grid, basin, r, c)
    basin_set = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if basin[r][c] is not None:
                basin_set.add(frozenset(basin[r][c]))
    basin_list = sorted(list(basin_set), key=len)
    return elf.product([len(a) for a in basin_list[-3:]])


def find_basin(grid, basin, r, c, basin_set=None):
    if grid[r][c] == 9:
        return
    if basin[r][c] is not None:
        return
    if basin_set is None:
        basin_set = set()
    basin_set.add((r, c))
    basin[r][c] = basin_set
    for rd, cd in elf.around_indexes(grid, r, c):
        find_basin(grid, basin, rd, cd, basin_set)


if __name__ == '__main__':
    main()
