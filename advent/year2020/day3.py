from advent.elf import read_lines, product


def main():
    part1(read_lines(__file__, list, True))
    part1(read_lines(__file__, list))
    part2(read_lines(__file__, list, True))
    part2(read_lines(__file__, list))


def part1(rows):
    print(trees_hit([3, 1], rows))


def trees_hit(slope, rows):
    run, rise = slope
    hit = 0
    x = 0
    for y in range(0, len(rows), rise):
        row = rows[y]
        if row[x % len(row)] == '#':
            hit += 1
        x += run
    return hit


def part2(rows):
    slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    print(product([trees_hit(slope, rows) for slope in slopes]))


if __name__ == '__main__':
    main()
