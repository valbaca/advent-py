from advent import elf


# Runs slow, gets the job done

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

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def rotate(dir):
    idx = DIRS.index(dir)
    return DIRS[(idx+1) % len(DIRS)]

class Grid:
    def __init__(self, grid):
        self.grid = grid

    def valid_nxt(self, nxt):
        return 0 <= nxt[0] < len(self.grid) and 0 <= nxt[1] < len(self.grid[0])

    def next_move(self, curr, dir):
        nxt = (curr[0]+dir[0], curr[1]+dir[1])
        if self.valid_nxt(nxt) and self.grid[nxt[0]][nxt[1]] == '#':
            new_dir = rotate(dir)
            return curr, new_dir
        else:
            return nxt, dir


def part1(lines):
    g = Grid([list(line) for line in lines])
    start = None
    for r, row in enumerate(g.grid):
        for c, ch in enumerate(row):
            if ch == '^':
                start = (r, c)
    curr, curr_face = start, DIRS[0]
    seen = {(curr, curr_face)}
    nxt, nxt_face = g.next_move(curr, curr_face)
    while g.valid_nxt(nxt) and (nxt, nxt_face) not in seen:
        curr, curr_face = nxt, nxt_face
        seen.add((curr, curr_face))
        nxt, nxt_face = g.next_move(curr, curr_face)
    return len(set(pos for pos, _ in seen))


def part2(lines):
    orig = Grid([list(line) for line in lines])
    total = 0
    for r, row in enumerate(orig.grid):
        for c, ch in enumerate(row):
            if ch == '^':
                start = (r, c)
    for r0, row0 in enumerate(orig.grid):
        for c0, ch0 in enumerate(row0):
            # if ch0 == '#' or ch0 == '^': # no idea why I needed to remove this
            #     break
            g = Grid([list(line) for line in lines])

            g.grid[r0][c0] = '#'

            curr, curr_face = start, DIRS[0]
            seen = {(curr, curr_face)}
            nxt, nxt_face = g.next_move(curr, curr_face)
            while g.valid_nxt(nxt) and (nxt, nxt_face) not in seen:
                curr, curr_face = nxt, nxt_face
                seen.add((curr, curr_face))
                nxt, nxt_face = g.next_move(curr, curr_face)
            if (nxt, nxt_face) in seen:
                total += 1
    return total


if __name__ == '__main__':
    main()
