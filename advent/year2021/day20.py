from advent import elf

"""
TIL: pay special attention to the problem emphasis.
The "infinite" matter suggested that the background would impact and it did.
The "algorithm's" zero value was actually '#'.
By printing  out the results, I saw the edges were always getting turned on, which indicated
the entire background was flashing on and off.

Thankfully I'd already built in a `default` value into my `at` function.
This made it easy to to swap out 0 with algo[0] or algo[-1] for last.
"""

def main():
    lines = elf.read_lines(__file__)
    print("Part 1:")
    print(part1(lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    return run(lines, 2)

def part2(lines):
    return run(lines, 50)

def run(lines, n):
    grid = init_grid(lines)
    for _ in range(n):
        grid = grid.next()
    return grid.count_on()

def init_grid(lines):
    algo = [1 if c == '#' else 0 for c in lines[0]]
    rest = lines[1:]
    larger_size = max(len(rest), len(rest[0]))
    grid = Grid(larger_size, algo)
    for iline, line in enumerate(rest):
        for ichar, char in enumerate(line):
            grid.grid[iline][ichar] = 1 if char == '#' else 0
    return grid

class Grid:
    def __init__(self, size, algo, it=0):
        self.size = size
        self.grid = [list(0 for _ in range(size)) for _ in range(size)]
        self.algo = algo
        self.it = it
    
    def at(self, r, c):
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[r]):
            return self.grid[r][c]
        # This next line was the gimmick. algo[0] is '#' which means all the background pixels
        # flash all ON and then algo[last] is '.' so they all turn off!
        # keeping track of the iterations allows us to remain "finite"
        return self.algo[0] if self.it % 2 != 0 else self.algo[-1]
    
    def calc_index(self, r, c):
        index = 0
        for rd in [-1, 0, 1]:
            for cd in [-1, 0, 1]:
                index <<= 1
                index += self.at(r+rd, c+cd)
        return index

    def next_pixel(self, r, c):
        idx = self.calc_index(r, c)
        return self.algo[idx]
    
    def next(self):
        expand = Grid(self.size+4, self.algo, self.it+1)
        for r, row in enumerate(expand.grid):
            for c in range(len(row)):
                expand.grid[r][c] = self.next_pixel(r-2, c-2)
        return expand

    def count_on(self):
        return sum([val for row in self.grid for val in row])

    def __str__(self):
        out = ""
        for row in self.grid:
            for val in row:
                out += "#" if val == 1 else '.'
            out += "\n"
        out += "\n"
        out += f"{self.size} {self.count_on()}"
        return out

if __name__ == '__main__':
    main()
