from advent import elf

"""
Prefix Sums FTW!
"""

def main():
    test_lines = elf.read_lines(__file__, parser=elf.safe_atoi, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__, parser=elf.safe_atoi)
    print("Part 1:", part1(lines))

    print("Part 2 (test):", part2(test_lines))
    print("Part 2:", part2(lines))


def part1(lines):
    count = 0
    for i, e in enumerate(lines):
        if i == 0:
            continue
        if e > lines[i - 1]:
            count += 1
    return count


def part2(lines):
    # Using prefix sums to make the sliding sum operations a single operation
    pref = [0] + lines[:]
    for i in range(1, len(pref)):
        pref[i] += pref[i - 1]
    count = 0
    for i in range(4, len(pref)):
        if (pref[i] - pref[i - 3]) > (pref[i - 1] - pref[i - 4]):
            count += 1
    return count


if __name__ == '__main__':
    main()
