from advent.elf import read_lines, septoi


class Grid:
    def __init__(self, i):
        self.grid = []
        for _ in range(i):
            self.grid.append([0 for _ in range(i)])

    def exec_range(self, x1, x2, y1, y2, lamb):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.grid[y][x] = lamb(self.grid[y][x])


def part1(input):
    g = Grid(1000)
    for line in input:
        s = septoi(line)
        if s[0] == "toggle":
            # toggle 0,0 through 999,0
            g.exec_range(s[1], s[4], s[2], s[5], lambda prev: 1 if prev == 0 else 0)
        elif s[1] == "on":
            # turn on 0,0 through 999,999
            g.exec_range(s[2], s[5], s[3], s[6], lambda _: 1)
        elif s[1] == "off":
            g.exec_range(s[2], s[5], s[3], s[6], lambda _: 0)
    return sum(sum(row) for row in g.grid)


def part2(input):
    g = Grid(1000)
    for line in input:
        s = septoi(line)
        if s[0] == "toggle":
            # toggle 0,0 through 999,0
            g.exec_range(s[1], s[4], s[2], s[5], lambda prev: prev + 2)
        elif s[1] == "on":
            # turn on 0,0 through 999,999
            g.exec_range(s[2], s[5], s[3], s[6], lambda prev: prev + 1)
        elif s[1] == "off":
            g.exec_range(s[2], s[5], s[3], s[6], lambda prev: 0 if prev == 0 else prev - 1)
    return sum(sum(row) for row in g.grid)


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
