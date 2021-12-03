from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2 (test):", part2(test_lines))

    print("Part 2:", part2(lines))


def part1(lines):
    counts = [0] * len(lines[0])
    for line in lines:
        for i, c in enumerate(line):
            if c == '1':
                counts[i] += 1
    gamma = ''
    epsilon = ''
    for i, count in enumerate(counts):
        if count > len(lines) // 2:
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    print(f"g={gamma} ep={epsilon}")
    return int(gamma, 2) * int(epsilon, 2)


def most_commons(lines, pos, want_most_common=True):
    if len(lines) == 1:
        return lines
    count1 = 0
    for line in lines:
        if line[pos] == '1':
            count1 += 1
    one_most = count1 > len(lines) // 2
    want_one = one_most
    if len(lines) % 2 == 0 and count1 == len(lines) // 2:
        want_one = True
    if not want_most_common:
        want_one = not want_one
    want = '1' if want_one else '0'
    return [line for line in lines if line[pos] == want]


def part2(lines):
    slines = sorted(lines)
    l = len(slines[0])
    oxy = slines[:]
    for i in range(l):
        oxy = most_commons(oxy, i)
    oxy_rating = int(oxy[0], 2)
    co2 = slines[:]
    for i in range(l):
        co2 = most_commons(co2, i, False)
    co2_rating = int(co2[0], 2)
    print(f"oxy rating = {oxy_rating} co2 rating = {co2_rating}")
    return oxy_rating * co2_rating

if __name__ == '__main__':
    main()
