from advent import elf

"""
TIL: like a lot of advent problems, best to avoid an actual grid until you need it.
Use a list/set of points instead.
Also, using `s in line` is Just Nice and straightforward (compared to .contains or .includes).
It reads more like how you would describe
"""


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
    grid = []
    dirs = []
    for line in lines:
        if "," in line:
            xy = line.split(",")
            x, y = xy
            grid.append([int(x), int(y)])
        elif "along" in line:
            _, _, xyz = line.split(" ")
            xy, z = xyz.split("=")
            dirs.append((xy, int(z)))
    return grid, dirs


def fold_dot(x, y, x_or_y, z):
    if x_or_y == "x":
        return [z - abs(z - x), y]
    elif x_or_y == "y":
        return [x, z - abs(z - y)]
    else:
        raise Exception("bad xy")


def fold(grid, dir):
    x_or_y, z = dir
    out_grid = []
    for x, y in grid:
        out_grid.append(fold_dot(x, y, x_or_y, z))
    return out_grid


def part1(lines):
    grid, dirs = parse(lines)
    grid = fold(grid, dirs[0])
    grid_tuples = [tuple(dot) for dot in grid]
    return len(set(grid_tuples))


def part2(lines):
    grid, dirs = parse(lines)
    for d in dirs:
        grid = fold(grid, d)
    grid_tuples = [tuple(dot) for dot in grid]
    max_x = max([x for x, _ in grid_tuples]) + 1
    max_y = max([y for _, y in grid_tuples]) + 1
    dgrid = [['.' for _ in range(max_x)] for _ in range(max_y)]
    for x, y in grid_tuples:
        dgrid[y][x] = '#'
    return "\n".join([" ".join(row) for row in dgrid])


if __name__ == '__main__':
    main()
