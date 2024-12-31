from advent import elf
from advent.elf import mv, get

# Definitely a challenging one to code up. Simple to understand and do by hand, but very tricky to code up right
# I am a bit proud of the "algorithms" I came up with for the perimeter calculations for part 1 and 2
# I was tempted to just look up a hint but figured it out on my own
# Also added a new helper function: get. Simply gives the value, if any. Surely I've come up with this before...

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


# Find the islands/regions
# Calc the perimeter


def perimeter(g, region, v):
    # for perimeter: just look around and add one fence for each non-same next-square, including out-of-bounds
    total = 0
    for r, c in region:
        for r2, c2 in elf.around_indexes(g, r, c):
            v2 = g[r2][c2]
            if v != v2:
                total += 1
        # around_indexes only goes through the actual values
        # below we do edge checks
        if r == 0:
            total += 1
        if r == len(g) - 1:
            total += 1
        if c == 0:
            total += 1
        if c == len(g[r]) - 1:
            total += 1
    return total


def shared(lines, perimeter_fn=perimeter):
    g = [list(line) for line in lines]

    acc = set()  # accounted for
    total = 0
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if (r, c) in acc:
                continue
            q = [(r, c)]
            region = {(r, c)}
            while q:
                r2, c2 = q.pop()
                for r3, c3 in elf.around_indexes(g, r2, c2):
                    v3 = g[r3][c3]
                    if v3 == v and (r3, c3) not in region:
                        q.append((r3, c3))
                        region.add((r3, c3))
            acc = acc.union(region)
            perim = perimeter_fn(g, region, v)
            price = (len(region) * perim)
            # print(f"region of {v} with price {len(region)} * {perim} = {price}")
            total += price
    return total


def part1(lines):
    return shared(lines)

N = (-1, 0)
E = (0, 1)
S = (1, 0)
W = (0, -1)
DIRS = [N, E, S, W]


def part2_perimeter(g, region, v):
    """
    I imagine this kind of how the Brady Brunch looks at each other...

    The idea is if we sort the region, so we're traversing it left-to-right, top to bottom, then we can determine
    walls by checking if a previous plot already counted that wall.

    XA  seen as:  X1
    YA            Y2

    1 counts all the walls as "new" so it increments the total walls.
    2 looks left, sees Y but first looks up (to 1) and left (to X) and sees that 1 and X were different, so we don't
    count the left wall as "new"

    A  seen as: 1
    A           2

    ^ This is an easy case. 1 looks left and sees a new wall. 2 looks left and sees empty, so it just looks up.
    It sees an A above (1) and so it knows the left wall has been counted.
    """

    # WOW I HATE THIS! Getting this coded up was a hot-mess.
    total = 0
    rs = list(sorted(list(region)))
    for i, (r, c) in enumerate(rs):
        up, right, down, left = mv((r,c), N), mv((r,c), E), mv((r,c), S), mv((r,c), W)

        # left, look up to see if they've already 'counted' a left wall
        # we don't need to look down because we sorted the region
        if c == 0:
            if up not in rs[:i]:
                total += 1
        elif get(g,left) != v:
            up_left_v = get(g, mv(up, W))
            if up in rs[:i] and up_left_v is not None and up_left_v != get(g, up):
                ... # already counted this left wall
            else:
                total += 1
        # same, but for right
        if c == len(g[r]) - 1:
            if up not in rs[:i]:
                total += 1
        elif get(g,right) != v:
            up_right_v = get(g, mv(up, E))
            if up in rs[:i] and up_right_v is not None and up_right_v != get(g, up):
                ...
            else:
                total += 1

        # up, look left (and up)
        if r == 0:
            if left not in rs[:i]:
                total += 1
        elif get(g, up) != v:
            left_up_v = get(g, mv(left, N))
            if left in rs[:i] and left_up_v is not None and left_up_v != get(g, left):
                ...
            else:
                total += 1
        # down, look left (and down)
        if r == len(g) - 1:
            if left not in rs[:i]:
                total += 1
        elif get(g, down) != v:
            left_down_v = get(g, mv(left, S))
            if left in rs[:i] and left_down_v is not None and left_down_v != get(g, left):
                ...
            else:
                total += 1
    return total


def part2(lines):
    return shared(lines, part2_perimeter)


if __name__ == '__main__':
    main()
