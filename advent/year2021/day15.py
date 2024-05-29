from heapq import heappop, heappush
from math import inf

from advent import elf

"""
TIL: a bit of a tough one, but A* is a champ. Part 2 was just more tedious than hard.
Incredibly surprised the soln runs in only about a second. Heaps FTW.
"""


def main():
    lines = elf.read_lines(__file__)
    print("Part 1:")
    print(part1(lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    grid = [[elf.safe_atoi(c) for c in list(line)] for line in lines]
    return lowest_risk_path(grid)


def lowest_risk_path(grid):
    visited = [[inf] * len(row) for row in grid]
    pq = [(0, 0, 0, 0)]  # (calc score, risk, r, c)
    while len(pq) > 0:
        _, risk, r, c = heappop(pq)
        if risk > visited[r][c]:
            continue
        visited[r][c] = risk
        for rr, cc in elf.around_indexes(grid, r, c):
            rrisk = grid[rr][cc] + risk
            if rrisk < visited[rr][cc]:
                heappush(pq, (calc_score(rrisk, rr, cc), rrisk, rr, cc))
    return visited[-1][-1]


# LOWEST score is the best path (want lowest b/c heap is a min-heap)
def calc_score(risk, r, c):
    # The 2 is a heuristic weight to push answers toward the bottom right. GREATLY speeds up soln
    return (risk) - ((r + c) * 2)


def part2(lines):
    grid = []
    for line in lines:
        grid.append([elf.safe_atoi(c) for c in list(line)])
    super_grid = []
    for r in range(len(grid) * 5):
        incr, ri = divmod(r, len(grid))
        super_grid.append(create_super_row(grid[ri], incr))
    return lowest_risk_path(super_grid)


def create_super_row(row, row_incr):
    srow = []
    for i in range(len(row) * 5):
        col_incr, ri = divmod(i, len(row))
        val = row[ri] + col_incr + row_incr
        val = ((val - 1) % 9) + 1  # to keep within range [1,9] ~= [0,8] + 1
        srow.append(val)
    return srow


if __name__ == '__main__':
    main()
