from collections import defaultdict
from math import inf
from advent import elf

"""SO glad I moved Dijkstra to a function. Using just a grid of the distances really helped this one be easier"""


def main():
    lines = elf.read_lines(__file__)
    dists = calc_dists(lines)
    print("Part 1:")
    print(part1(dists))
    print("Part 2:")
    print(part2(dists))

def calc_dists(lines):
    grid = [list(line) for line in lines]
    start = [(r,c) for r,c,v in elf.iter_grid(grid) if v == 'S'][0]
    grid[start[0]][start[1]] = '.'
    end = [(r,c) for r,c,v in elf.iter_grid(grid) if v == 'E'][0]
    grid[end[0]][end[1]] = '.'

    dij = elf.Dijkstra(grid)
    dists = dij.dijkstra(start)
    return dists

def part1(dists):
    min_saved = 100
    cheats_count = defaultdict(int)
    cheats = set()
    for r,c,d in elf.iter_grid(dists):
        if d == inf: # cannot cheat FROM walls
            continue
        for dir in elf.DIRS:
            r1 = r+dir[0]
            c1 = c+dir[1]
            if 0 <= r1 < len(dists) and 0 <= c1 < len(dists[r1]) \
                and dists[r1][c1] == inf: # only cheat through walls
                r2, c2 = r+2*dir[0], c+2*dir[1]
                if 0 <= r2 < len(dists) and 0 <= c2 < len(dists[r2]) \
                    and dists[r2][c2] != inf: # cannot end on a wall
                    d2 = dists[r2][c2]
                    saved =  d - d2 - 2
                    if saved >= min_saved:
                        cheats.add(((r1,c1), (r2,c2)))
                        cheats_count[saved] += 1
    return len(cheats)


def part2(dists):
    cheats = set()
    n = 20 # cheat len
    target = 100 # save at least 100 picoseconds

    def check(r,c,d,r2,c2):
        d2 = dists[r2][c2]
        if d2 == inf:
            return # cannot end on a wall
        md = abs(r-r2) + abs(c-c2) # manhattan distance
        saved = (d2 - d) - md
        if saved >= target:
            cheats.add(((r,c), (r2,c2)))

    for r,c,d in elf.iter_grid(dists):
        # for each position, look "up" (then left and right) up to the manhattan dist of n
        if d == inf:
            continue # cannot cheat from walls
        """
        ...8...
        ..657..
        .21034.  # we're looking at 0, and goes in order of 123456789ABC except up to 20 "around"
        ..A9B..
        ...C...
        """
        for rd in range(0, n+1):
            r2 = r-rd # going up
            if 0 <= r2 < len(dists):
                for cd in range(0, n-rd+1):
                    c2 = c-cd # going left
                    if (0 <= c2 < len(dists[r2])):
                        check(r,c,d,r2,c2)
                    c2 = c+cd # going right
                    if (0 <= c2 < len(dists[r2])):
                        check(r,c,d,r2,c2)
            r2 = r+rd # going down
            if 0 <= r2 < len(dists):
                for cd in range(0, n-rd+1):
                    c2 = c-cd # going left
                    if (0 <= c2 < len(dists[r2])):
                        check(r,c,d,r2,c2)
                    c2 = c+cd # going right
                    if (0 <= c2 < len(dists[r2])):
                        check(r,c,d,r2,c2)
    return len(cheats)


if __name__ == '__main__':
    main()
