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
    return fast_count_fish(lines, 80)


def count_fish(lines, days):
    """This isn't used since it didn't scale to part 2, but keeping for show"""
    fish = elf.septoi(lines[0])
    for _ in range(days):
        new_fish = 0
        n = len(fish)
        for i in range(n):
            f = fish[i]
            if f == 0:
                new_fish += 1
                fish[i] = 6
            else:
                fish[i] = f - 1
        for x in range(new_fish):
            fish.append(8)
    return len(fish)


def part2(lines):
    return fast_count_fish(lines, 256)


def fast_count_fish(lines, days):
    "Using an array to keep count of the # of fish in each generation, where the index is the # of days to reproduce"
    fish = elf.septoi(lines[0])
    gens = [0] * 9
    for f in fish:
        gens[f] += 1
    print(gens)
    for _ in range(days):
        new_gens = [0] * 9
        # move each generation "forward" a day
        for i in range(1, len(gens)):
            new_gens[i - 1] += gens[i]
        new_gens[6] += gens[0]  # reset the birthing generation
        new_gens[8] += gens[0]  # new spawn
        gens = new_gens
    return sum(gens)


if __name__ == '__main__':
    main()
