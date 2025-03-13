from collections import defaultdict
from math import inf
from typing import Counter
from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    # print("Part 2 (test):")
    # print(part2(test_lines))
    # print("Part 2:")
    # print(part2(lines))


def part1(lines):
    grid = [list(line) for line in lines]
    start = [(r,c) for r,c,v in elf.iter_grid(grid) if v == 'S'][0]
    grid[start[0]][start[1]] = '.'
    end = [(r,c) for r,c,v in elf.iter_grid(grid) if v == 'E'][0]
    grid[end[0]][end[1]] = '.'

    dij = elf.Dijkstra(grid)
    dists = dij.dijkstra(start)
    print("calculated distances...")

    # return elf.get(dists, end) # verified Dij still works
    cheats = defaultdict(int)
    min_saved = 100
    # cheats = 0
    # cheats = Counter()
    for r,c,d in elf.iter_grid(dists):
        if d == inf: # cannot cheat FROM walls
            continue
        for dir in elf.DIRS:
            r1 = r+dir[0]
            c1 = c+dir[1]
            if 0 <= r1 < len(dists) and 0 <= c1 < len(dists[r1]) \
                and dists[r1][c1] == inf: # only cheat through walls
                r2 = r+2*dir[0]
                c2 = c+2*dir[1]
                if 0 <= r2 < len(dists) and 0 <= c2 < len(dists[r1]) \
                    and dists[r2][c2] != inf: # cannot end on a wall
                    saved = d - dists[r2][c2]
                    if saved > 0:
                        cheats[saved] += 1
                    # if saved >= min_saved:
                        # cheats += 1
    print("calculated cheats...")
    return sum(v for k,v in cheats.items() if k >= 100)
# 1498 too high


def part2(lines):
    ...


if __name__ == '__main__':
    main()
