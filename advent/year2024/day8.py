from collections import defaultdict

from advent import elf


# This was a pretty easy one, again, thanks to Python Tuples making it easy to deal with x,y or r,c coordinates in a set

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

def dist2d(a, b):
    return a[0] - b[0], a[1] - b[1]

def part1(lines):
    return shared_part(lines)

def shared_part(lines, is_part1=True):
    g = [list(line) for line in lines] # grid
    ants = defaultdict(set) # antennas
    for r, row in enumerate(g):
        for c, ch in enumerate(row):
            if ch != '.':
                ants[ch].add((r, c))


    found = set()
    for name in ants:
        stations = list(ants[name])
        # start from station a, look at all others (b). Also look at a from b
        for i, a in enumerate(stations):
            for j, b in enumerate(stations[i+1:]):
                find_antinode(a, b, found, g, is_part1)
                find_antinode(b, a, found, g, is_part1)
    return len(found)


def find_antinode(a, b, found, g, is_part1):
    # for part 1, we just look at one "antinode"/resonance away. For part 2, we go through all.
    times = [1] if is_part1 else range(len(g))
    df = dist2d(a, b)
    for t in times:
        ax = a[0] + df[0]*t, a[1] + df[1]*t
        if 0 <= ax[0] < len(g) and 0 <= ax[1] < len(g[ax[0]]):
            found.add(ax)


def part2(lines):
    return shared_part(lines, False)


if __name__ == '__main__':
    main()
