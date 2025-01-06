from math import inf

from advent import elf

# LOVE how easy this one was with just two algorithms:
# - Dijkstra's for the path finding
# - Binary Search for quickly finding the first block (similar to `git bisect`)
# This is likely to be my favorite puzzle of the year
# Also, finally have a short example of Dijkstra's

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines, size=6, bytes=12))
    print("Part 1:")
    print(part1(lines, size=70, bytes=1024))
    print("Part 2 (test):")
    print(part2(test_lines, size=6))
    print("Part 2:")
    print(part2(lines, size=70))


def part1(lines, size, bytes):
    g = [['.'] * (size + 1) for _ in range(size + 1)]
    for line in lines[:bytes]:
        c, r = elf.septoi(line)
        g[c][r] = '#'
    dij = Dijkstra(g)
    return dij.dijkstra((0, 0))[size][size]


class Dijkstra:
    def __init__(self, grid):
        self.grid = grid

    def dijkstra(self, start):
        # start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [[inf] * len(self.grid) for _ in range(len(self.grid))]
        distances[start[0]][start[1]] = 0
        visited = [[False] * len(self.grid) for _ in range(len(self.grid))]

        for _, _ in elf.iter_grid_indexes(self.grid):
            min_distance = inf

            u = None  # the node we inspect next...
            for r, c in elf.iter_grid_indexes(self.grid):
                if not visited[r][c] and distances[r][c] < min_distance:
                    min_distance = distances[r][c]
                    u = r, c
            if u is None:
                break

            visited[u[0]][u[1]] = True

            for r, c in elf.around_indexes(self.grid, u[0], u[1]):
                if self.grid[r][c] != '#' and not visited[r][c]:
                    alt = distances[u[0]][u[1]] + 1
                    if alt < distances[r][c]:
                        distances[r][c] = alt
        return distances


def part2(lines, size):
    lo, hi = 0, len(lines)
    p2_ans = None
    while lo != hi:
        b = (lo + hi) // 2
        ans = part1(lines, size=size, bytes=b)
        print(f"{b=} => {ans=} ... {lines[b - 1]}")
        if ans == inf:
            hi = b
            p2_ans = lines[b - 1]
        else:
            lo = b + 1
    return p2_ans


if __name__ == '__main__':
    main()
