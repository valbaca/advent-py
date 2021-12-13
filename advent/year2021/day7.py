import math

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


def calc_fuel(positions, target_pos):
    return sum((abs(target_pos - pos) for pos in positions))


def part1(lines, calc_fuel_fn=calc_fuel):
    positions = elf.septoi(lines[0])
    mn, mx = min(positions), max(positions)
    min_fuel = math.inf
    min_fuel_pos = None
    for target_pos in range(mn, mx + 1):
        fuel = calc_fuel_fn(positions, target_pos)
        if min_fuel > fuel:
            min_fuel = fuel
            min_fuel_pos = target_pos
    return min_fuel, min_fuel_pos


def crab_calc_fuel(positions, target_pos):
    normal_fuel = (abs(target_pos - pos) for pos in positions)
    crab_fuel = (n * (n + 1) // 2 for n in normal_fuel)
    return sum(crab_fuel)


def part2(lines):
    return part1(lines, crab_calc_fuel)


if __name__ == '__main__':
    main()
