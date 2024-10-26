import numpy as np

from advent import elf


# TIL: huge help from numpy in this one, simplified a lot of grid work
# Reminding me why Python is great!!! (when it is great)

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


def helper(lines, expansion=1):
    grid = np.array([list(line) for line in lines])
    galaxies = list(zip(*np.where(grid == '#'))) # list of row,col tuples
    empty_cols = np.where(np.all(grid == '.', axis=0))[0]
    empty_rows = np.where(np.all(grid == '.', axis=1))[0]

    def calc_distance(src, dst):
        lo_row, hi_row = min(src[0], dst[0]), max(src[0], dst[0])
        row_range = range(lo_row, hi_row + 1)
        row_expansion = sum(expansion for empty_row in empty_rows if empty_row in row_range)
        lo_col, hi_col = min(src[1], dst[1]), max(src[1], dst[1])
        col_range = range(lo_col, hi_col + 1)
        col_expansion = sum(expansion for empty_col in empty_cols if empty_col in col_range)
        return (hi_row - lo_row) + (hi_col - lo_col) + row_expansion + col_expansion

    return sum(
        calc_distance(galaxy, other_galaxy)
        for g, galaxy in enumerate(galaxies)
        for other_galaxy in galaxies[g+1:] # python is nice and if you slice beyond, gives an empty slice!
    )

def part1(lines):
    return helper(lines)

def part2(lines):
    return helper(lines, expansion=1000000-1) # -1 bc we count the original row/col as part of the dist formula


if __name__ == '__main__':
    main()
