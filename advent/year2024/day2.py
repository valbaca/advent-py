from advent import elf


# Just brute-forced this one. *shrug*

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


def is_safe(report):
    # found this easier to reason about: generate all the diffs then apply the rules basically verbatim:
    # all increasing/decreasing and all within [1,3]
    diffs = [b-a for a, b in zip(report, report[1:])]
    return (all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs)) and all(1 <= abs(diff) <= 3 for diff in diffs)

def is_semi_safe(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False

def part1(lines):
    reports = [elf.septoi(line) for line in lines]
    return len([1 for report in reports if is_safe(report)])


def part2(lines):
    reports = [elf.septoi(line) for line in lines]
    return len([1 for report in reports if is_semi_safe(report)])


if __name__ == '__main__':
    main()
