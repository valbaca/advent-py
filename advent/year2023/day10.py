from collections import deque
from heapq import heappush, heappop
from advent import elf


# TIL: a quick way to determine "in"/"out" of a loop
# Part 2 fully stumped me and I had to go find a solution and translate it
# Luckily the way I had done part 1 was easy to adapt to their approach

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


# directions
N = (-1, 0)
W = (0, -1)
E = (0, 1)
S = (1, 0)
# Notice the directions are sorted by their tuple values. This helps with comparisons later
ALL_DIRS = [N, W, E, S]
OPPOSITES = {N: S, S: N, W: E, E: W}


pipes = {
    'S': None,
    '.': None,
    # again, notice the directions are in-direction-sorted order
    '|': [N, S],
    '-': [W, E],
    'L': [N, E],
    'J': [N, W],
    '7': [W, S],
    'F': [E, S],
}


# "coordinate plus": given `a` (a coordinate) and `b` (a direction) returns a new coordinate of them added
def cplus(a, b):
    return a[0] + b[0], a[1] + b[1]


def find_start(grid):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == 'S':
                return r, c


# given a start position `a` and a given direction `dir`: determine if pipe a is connected to b
# very suboptimal
def is_connected(grid, a, dir, start=False):
    b = cplus(a, dir)
    if not (0 <= b[0] < len(grid) and 0 <= b[1] < len(grid[0])):
        return False
    b_char = grid[b[0]][b[1]]
    # is b connected to a
    b_pipe = pipes[b_char]
    if not b_pipe:
        return False
    b_pipe_opps = [OPPOSITES[b_char] for b_char in b_pipe]
    if dir not in b_pipe_opps:
        return False
    # see if a is connected to b
    if start:
        return True
    a_char = grid[a[0]][a[1]]
    a_pipe = pipes[a_char]
    return dir in a_pipe


def part1(lines):
    return helper(lines)[0]


# extracted out the common logic between the two parts of traversing the grid and find what parts are the pipe-loop
def helper(lines):
    grid = [[c for c in list(line)] for line in lines]
    start = find_start(grid)
    q = []  # queue to traverse the pipes, each element is (dist: int, coordinate) where coordinate is (row: int, col: int)
    # using a heap to ensure we're traversing in a breadth-first fashion
    actual_pipes = set()  # coordinates of the pipes
    actual_pipes.add(start)

    # start is a little special, look around it to figure out what "shape" it is
    start_dirs = []
    for d in ALL_DIRS:
        if is_connected(grid, start, d, start=True):
            start_dirs.append(d)
            coor = cplus(start, d)
            actual_pipes.add(coor)
            heappush(q, (1, coor))
    for (k, v) in pipes.items():
        if v == start_dirs: # This is where ordering the directions and keeping them in order pays off
            print("Detected that the S start should be " + k)
            grid[start[0]][start[1]] = k  # replace the 'S' with what "shape" it ought to be
    seen = set()
    seen.add(start)

    furthest = 1  # furthest distance from start
    while q:
        dist, coor = heappop(q)
        if coor in seen:
            continue
        seen.add(coor)
        # print(f"Looking at {grid[coor[0]][coor[1]]} at r={coor[0]} c={coor[1]}; dist={dist}")
        for d in pipes[grid[coor[0]][coor[1]]]:
            potential = cplus(coor, d)
            if potential not in seen and is_connected(grid, coor, d):
                actual_pipes.add(potential)
                heappush(q, (dist + 1, potential))
                furthest = max(furthest, dist + 1)
    return furthest, grid, actual_pipes


# "borrowed" this approach from
# https://www.reddit.com/r/adventofcode/comments/18ey1s7/comment/kcr3x2c/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://github.com/fred-corp/Advent-of-Code/blob/main/2023/day10/day10.js
def part2(lines):
    _, grid, actual_pipes = helper(lines)
    count = 0
    for r, row in enumerate(grid):
        in_loop = False
        prev_ch = None
        for c, ch in enumerate(row):
            if (r, c) in actual_pipes:
                if ch != '-':
                    in_loop = not in_loop
                    if ch == 'J' and prev_ch == 'F' or ch == '7' and prev_ch == 'L':
                        in_loop = not in_loop
                    prev_ch = ch
            elif in_loop:
                count += 1
    return count


if __name__ == '__main__':
    main()
