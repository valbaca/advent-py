from advent.elf import lines


def part1(ints):
    set_ints = set(ints)
    found = None
    for i in ints:
        seek = 2020 - i
        if seek in set_ints:
            found = seek * i
    return found


def part2(ints):
    set_ints = set(ints)
    found = None
    for i in ints:
        for j in ints:
            if i != j:
                seek = 2020 - (i + j)
                if seek in set_ints:
                    found = seek * i * j
    return found


if __name__ == '__main__':
    # print(f"test: {part1(test_lines(__file__, int))}")
    print(f"Part 1: {part1(lines(__file__, int))}")
    # print("test: " + part2(test_lines(__file__, int)))
    print(f"Part 2: {part2(lines(__file__, int))}")