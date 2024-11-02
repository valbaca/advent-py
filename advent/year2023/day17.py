import dataclasses
from dataclasses import dataclass
from math import inf

from boltons.queueutils import PriorityQueue

from advent import elf


"""
Really pushing the boundaries of "brute-force" here.

I tackle this the same way I tackle a lot of (the grid) problems:
- priority queue of work to do
- set of work done, so we don't repeat work

There's undoubtedly a more optimal way to do this. I'm (sort-of) doing BFS and DFS would likely be better.
Also this code's quite a mess.

But damn. computers are fast and python is easy 
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


N = (-1, 0)
W = (0, -1)
E = (0, 1)
S = (1, 0)

CARDINAL = [N, E, S, W]  # clockwise order


def part1(lines):
    g = [list(int(ch) for ch in line)
         for line in lines]

    def in_grid(loc):
        return 0 <= loc[0] < len(g) and 0 <= loc[1] < len(g[0])

    @dataclass(frozen=True, slots=True)
    class Crucible:
        loc: tuple[int, int]  # location: r,c
        d: tuple[int, int]  # N W E S
        heat: int = 0 # how much heat has been gathered
        n: int = 2  # how many "straight" steps allowed

        def get_moves(self):
            moves = []
            if self.n > 0:
                floc = self.loc[0] + self.d[0], self.loc[1] + self.d[1]
                if in_grid(floc):
                    new_heat = self.heat + g[floc[0]][floc[1]]
                    moves.append(Crucible(floc, self.d, new_heat, self.n - 1))
            rd = CARDINAL[(CARDINAL.index(self.d) + 1) % len(CARDINAL)]
            rloc = self.loc[0] + rd[0], self.loc[1] + rd[1]
            if in_grid(rloc):
                new_heat = self.heat + g[rloc[0]][rloc[1]]
                moves.append(Crucible(rloc, rd, new_heat))
            ld = CARDINAL[(CARDINAL.index(self.d) - 1) % len(CARDINAL)]
            lloc = self.loc[0] + ld[0], self.loc[1] + ld[1]
            if in_grid(lloc):
                new_heat = self.heat + g[lloc[0]][lloc[1]]
                moves.append(Crucible(lloc, ld, new_heat))
            return moves

        def priority(self):
            return -self.heat

    q = PriorityQueue()
    q.add(Crucible((0, 0), E), 0)
    q.add(Crucible((0, 0), S), 0)
    min_heat = inf
    goal_loc = (len(g) - 1, len(g[0]) - 1)
    seen = {}
    while q:
        b = q.pop()

        key = dataclasses.replace(b, heat=-1)
        if key in seen:
            if seen[key] < b.heat:
                continue
        seen[key] = b.heat

        if b.heat >= min_heat:
            continue

        if b.loc == goal_loc:
            min_heat = min(min_heat, b.heat)
            continue

        for move in b.get_moves():
            q.add(move, move.priority())
    return min_heat


def part2(lines):
    """Mostly copied from part1"""
    g = [list(int(ch) for ch in line)
         for line in lines]

    def in_grid(loc):
        return 0 <= loc[0] < len(g) and 0 <= loc[1] < len(g[0])

    @dataclass(frozen=True, slots=True)
    class UltraCrucible:
        loc: tuple[int, int]  # location: r,c
        d: tuple[int, int]  # N W E S
        heat: int = 0
        n: int = 10  # how many "straight" steps allowed
        m: int = 4  # how many "straight" steps are REQUIRED

        def get_moves(self):
            moves = []
            if self.n > 0:
                if self.m == 4 and self.n >= 4:
                    floc = (self.loc[0] + (self.d[0] * 4), self.loc[1] + (self.d[1] * 4))
                    if in_grid(floc):
                        new_heat = self.heat
                        for x in range(1, 5):
                            temp_loc_row = self.loc[0] + (self.d[0] * x)
                            temp_loc_col = self.loc[1] + (self.d[1] * x)
                            new_heat += g[temp_loc_row][temp_loc_col]
                    ndiff = 4
                elif self.m == 0:
                    floc = self.loc[0] + self.d[0], self.loc[1] + self.d[1]
                    if in_grid(floc):
                        new_heat = self.heat + g[floc[0]][floc[1]]
                    ndiff = 1
                else:
                    floc = (-1, -1)  # skip
                if in_grid(floc):
                    moves.append(UltraCrucible(loc=floc, d=self.d, heat=new_heat, n=self.n - ndiff, m=0))

            # turn, n = 10, m = 4 => move 4, then re-eval
            rd = CARDINAL[(CARDINAL.index(self.d) + 1) % len(CARDINAL)]
            rloc = self.loc[0] + rd[0] * 4, self.loc[1] + rd[1] * 4
            if in_grid(rloc):
                # count up heat
                new_heat = self.heat
                for x in range(1, 5):
                    temp_loc_row = self.loc[0] + (rd[0] * x)
                    temp_loc_col = self.loc[1] + (rd[1] * x)
                    new_heat += g[temp_loc_row][temp_loc_col]
                moves.append(UltraCrucible(rloc, rd, new_heat, n=6, m=0))

            # same for left
            ld = CARDINAL[(CARDINAL.index(self.d) - 1) % len(CARDINAL)]
            lloc = self.loc[0] + ld[0] * 4, self.loc[1] + ld[1] * 4
            if in_grid(lloc):
                # count up heat
                new_heat = self.heat
                for x in range(1, 5):
                    temp_loc_row = self.loc[0] + (ld[0] * x)
                    temp_loc_col = self.loc[1] + (ld[1] * x)
                    new_heat += g[temp_loc_row][temp_loc_col]
                moves.append(UltraCrucible(lloc, ld, new_heat, n=6, m=0))
            return moves

        def priority(self):
            return -self.heat

    q = PriorityQueue()
    q.add(UltraCrucible((0, 0), E), 0)
    q.add(UltraCrucible((0, 0), S), 0)
    min_heat = inf
    goal_loc = (len(g) - 1, len(g[0]) - 1)
    seen = {}
    while q:
        b = q.pop()

        key = dataclasses.replace(b, heat=-1)
        if key in seen:
            if seen[key] <= b.heat:
                continue
        seen[key] = b.heat

        if b.heat >= min_heat:
            continue

        if b.loc == goal_loc:
            min_heat = min(min_heat, b.heat)
            continue

        moves = b.get_moves()
        for move in moves:
            q.add(move, move.priority())
    return min_heat


if __name__ == '__main__':
    main()
