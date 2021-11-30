from advent import elf


def main():
    lines = parse(elf.read_lines(__file__))
    print(part1(lines))
    lines = parse(elf.read_lines(__file__))
    print(part2(lines))


def parse(lines):
    return [list(line) for line in lines]


def count_occ_seats(g):
    t = 0
    for row in g:
        t += row.count('#')
    return t


def print_grid(g):
    for row in g:
        print(str.join("", row))
    print(count_occ_seats(g))


def occ_around(g, r, c):
    around = 0
    for rd in [-1, 0, 1]:
        for cd in [-1, 0, 1]:
            if rd == 0 and cd == 0:  # skip-self
                continue
            rr = r + rd
            if rr < 0 or rr >= len(g):
                continue
            row = g[rr]
            cc = c + cd
            if cc < 0 or cc >= len(row):
                continue
            char = g[rr][cc]
            if char == '#' or char == 'E':  # occupied or "was" occupied
                around += 1
    return around


def update(g, occ_fn=occ_around, *, occ_tolerance=4):
    updated = False
    # # = is occupied
    # L = is empty
    # O = becomes occupied (was empty)
    # E = becomes empty (was occupied)
    # . = floor
    for r in range(len(g)):
        row = g[r]
        for c in range(len(row)):
            char = g[r][c]
            if char == '.':
                continue
            elif char == '#' and occ_fn(g, r, c) >= occ_tolerance:
                g[r][c] = 'E'
                updated = True
            elif char == 'L' and occ_fn(g, r, c) == 0:
                g[r][c] = 'O'
                updated = True
    for r in range(len(g)):
        row = g[r]
        for c in range(len(row)):
            char = g[r][c]
            if char == 'E':
                g[r][c] = 'L'
            elif char == 'O':
                g[r][c] = '#'
    return updated, g


def part1(g):
    # print_grid(g)
    updated = True
    while updated:
        updated, g = update(g)
        # print_grid(g)
    return count_occ_seats(g)


def get_beyond(g, r, rd, c, cd):
    if rd == 0 and cd == 0:
        return None
    rr = r
    cc = c
    while True:
        rr += rd
        if rr < 0 or rr >= len(g):
            return None
        row = g[rr]
        cc += cd
        if cc < 0 or cc >= len(row):
            return None
        char = g[rr][cc]
        if char != '.':
            return char


def occ_beyond(g, r, c):
    around = 0
    for rd in [-1, 0, 1]:
        for cd in [-1, 0, 1]:
            char = get_beyond(g, r, rd, c, cd)
            if char == '#' or char == 'E':  # occupied or "was" occupied
                around += 1
    return around


def part2(g):
    print_grid(g)
    updated = True
    while updated:
        updated, g = update(g, occ_beyond, occ_tolerance=5)
        print_grid(g)
    return count_occ_seats(g)


if __name__ == '__main__':
    main()
