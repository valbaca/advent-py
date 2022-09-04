import advent.elf as elf


def part1(lines):
    dims = [sorted(elf.septoi(line, r"x")) for line in lines]
    ans = 0
    for lo,mi,hi in dims:
        ans += 2 * (lo * mi + mi * hi + lo * hi) + lo*mi
    return sum((2 * (lo * mi + mi * hi + lo * hi) + lo*mi) for lo, mi, hi in dims)


def part2(lines):
    dims = [sorted(elf.septoi(line, r"x")) for line in lines]
    return sum((2*(lo+mi) + (lo*mi*hi)) for lo, mi, hi in dims)


if __name__ == "__main__":
    print(part1(elf.read_lines(__file__)))
    print(part2(elf.read_lines(__file__)))
