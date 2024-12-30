from advent import elf


# Hilariously, I accidentally solved part 2 first while I misread part 1
# So solving part 2 was just going back to what I had before
# elf.around_indexes was handy

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
    g = []
    for line in lines:
        g.append([int(ch) for ch in line])

    total = 0
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 0:
                ends = trails(g, r, c, v)
                total += len(ends)
                # print(f"{len(ends)} => {total} @ {r}, {c}")
    return total


def trails(g, r, c, val):
    if val == 9:
        return {(r,c)}
    total = set()
    for nr, nc in elf.around_indexes(g, r, c):
        if val+1 == g[nr][nc]:
            total.update(trails(g, nr, nc, g[nr][nc]))
    return total



def part2(lines):
    g = []
    for line in lines:
        g.append([int(ch) for ch in line])

    total = 0
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 0:
                ends = trails_total(g, r, c, v)
                total += ends
                # print(f"{ends} => {total} @ {r}, {c}")
    return total


def trails_total(g, r, c, val):
    if val == 9:
        return 1
    total = 0
    for nr, nc in elf.around_indexes(g, r, c):
        if val+1 == g[nr][nc]:
            total += trails_total(g, nr, nc, g[nr][nc])
    return total

if __name__ == '__main__':
    main()
