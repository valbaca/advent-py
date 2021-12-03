from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)

    print("Part 1 (test):", part1(test_lines))
    print("Part 1:", part1(lines))

    print("Part 2 (test):", part2(test_lines))
    print("Part 2:", part2(lines))


def part1(lines):
    tlines = elf.transpose(lines[:])
    counts = [line.count('1') - line.count('0') for line in tlines]
    gamma = ''.join([('1' if count > 0 else '0') for count in counts])
    epsilon = ''.join([('1' if count <= 0 else '0') for count in counts])
    # print(f"g={gamma} ep={epsilon}")
    return int(gamma, 2) * int(epsilon, 2)


def common(lines, pos, want_most_common=True):
    if len(lines) == 1:
        return lines
    count1 = elf.transpose(lines)[pos].count('1')
    one_most = count1 > len(lines) // 2 or (len(lines) % 2 == 0 and count1 == len(lines) // 2)
    want_one = one_most
    if not want_most_common:
        want_one = not want_one
    want = '1' if want_one else '0'
    return [line for line in lines if line[pos] == want]


def part2(lines):
    n = len(lines[0])
    oxy = lines[:]
    for i in range(n):
        oxy = common(oxy, i)
    oxy_rating = int(oxy[0], 2)
    co2 = lines[:]
    for i in range(n):
        co2 = common(co2, i, False)
    co2_rating = int(co2[0], 2)
    # print(f"oxy rating = {oxy_rating} co2 rating = {co2_rating}")
    return oxy_rating * co2_rating


if __name__ == '__main__':
    main()
