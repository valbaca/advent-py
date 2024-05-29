from advent.elf import all_values_around, read_lines


def part1(input):
    grid = [list(line) for line in input]  # list(line) does line.split("")
    for _ in range(100):
        grid = next_grid(grid)
    return count_on(grid)


def next_grid(grid, corners_stuck=False):
    new = [['.'] * len(grid) for _ in range(len(grid))]
    for r, row in enumerate(grid):
        for c, prev in enumerate(row):
            new[r][c] = next_light(grid, prev, r, c)
    if corners_stuck:  # for part 2
        corners = [0, len(grid) - 1]
        for r in corners:
            for c in corners:
                new[r][c] = '#'
    return new


def next_light(grid, prev, r, c):
    neighbors_on = all_values_around(grid, r, c).count('#')
    if prev == '#' and (2 <= neighbors_on <= 3):
        return '#'
    elif prev == '.' and neighbors_on == 3:
        return '#'
    return '.'


def count_on(grid):
    return sum(row.count('#') for row in grid)


def part2(input):
    grid = [list(line) for line in input]  # list(line) does line.split("")
    corners = [0, len(grid) - 1]
    for r in corners:
        for c in corners:
            grid[r][c] = '#'
    for _ in range(100):
        grid = next_grid(grid, corners_stuck=True)
    return count_on(grid)


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
