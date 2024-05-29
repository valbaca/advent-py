from collections import namedtuple

from advent import elf


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


def part1(lines):
    ons = set()
    for seps in [elf.septoi(x) for x in lines]:
        execute(ons, seps)
    return len(ons)


def in_cube(lo, hi):
    # Given input values, returns a python range
    if lo > 50 or hi < -49:
        return []
    return range(
        max(lo, -50),
        min(hi + 1, 51)
    )


def execute(ons: set, seps):
    # ['on', 'x', -20, 26, 'y', -36, 17, 'z', -47, 7]
    for x in in_cube(seps[2], seps[3]):
        for y in in_cube(seps[5], seps[6]):
            for z in in_cube(seps[8], seps[9]):
                if seps[0] == 'on':
                    ons.add((x, y, z))
                else:
                    ons.discard((x, y, z))


# Part 2 start...

Cube = namedtuple('Cube', 'x y z')
FCube = namedtuple('FCube', 'flip cube')


def part2(lines):
    flip_cubes = [line_to_flip_cube(line) for line in lines]
    ons = []
    # I caved and based off another answer I found:
    # I was nearly there, had the intersection function but didn't think
    # of just storing the overlap cuboids and summing them all while 
    # keeping track of on/off and using 1/-1 multipliers.
    # https://tinyurl.com/yczcrdkg
    for fcube in flip_cubes:
        new_cubes = [fcube] if fcube.flip == 'on' else []
        for on in ons:
            overlap_size, overlap = overlap_cube(on.cube, fcube.cube)
            if overlap_size:
                flip = 'on' if on.flip == 'off' else 'off'
                new_cubes.append(FCube(flip, overlap))
        ons += new_cubes
    return count_on(ons)


def count_on(ons: list[FCube]):
    count = 0
    for on in ons:
        cube: Cube = on.cube
        count += ((1 if on.flip == 'on' else -1) * (
                (cube.x[1] - cube.x[0] + 1) * (cube.y[1] - cube.y[0] + 1) * (cube.z[1] - cube.z[0] + 1)))
    return count


def line_to_flip_cube(line) -> FCube:
    seps = elf.septoi(line)
    # ['on', 'x', -20, 26, 'y', -36, 17, 'z', -47, 7]
    return FCube(
        seps[0],
        Cube(
            (seps[2], seps[3]),  # x
            (seps[5], seps[6]),  # y
            (seps[8], seps[9]),  # z
        ))


def overlap_cube(a: Cube, b: Cube):
    # given two cubes determines overlap
    # returns the size of overlap (0 if none) and the cube by which they overlap
    overlaps = [overlap(a.x, b.x), overlap(a.y, b.y), overlap(a.z, b.z)]
    size = elf.product([overlap[0] for overlap in overlaps])
    if size == 0:
        return size, None
    return size, Cube(*[overlap[1] for overlap in overlaps])


def overlap(c, d):
    # given two ranges, returns their overlap size and overlap
    # c << d
    if c[1] < d[0]:
        return 0, ()
    # d << c
    if d[1] < c[0]:
        return 0, ()
    # c fully within d, then overlap is simply c
    if c[0] >= d[0] and c[1] <= d[1]:
        return c[1] - c[0] + 1, c
    # d fully within d, then overlap is simply d
    if d[0] >= c[0] and d[1] <= c[1]:
        return d[1] - d[0] + 1, d
    # c[0] is "lo" of overlap if it's within d
    if d[0] <= c[0] <= d[1]:
        lo = c[0]
        hi = min(c[1], d[1])
        return hi - lo + 1, (lo, hi)
    else:
        lo = d[0]
        hi = min(c[1], d[1])
        return hi - lo + 1, (lo, hi)


if __name__ == '__main__':
    main()
