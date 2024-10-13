from advent import elf


# TIL: glad I remembered my septoi helper to deal with split() giving empty strings, ugh.
# As with fibonacci, building bottom up ~ dynamic programming ~ works best
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
    return sum(score(line) for line in lines)

def winners(have, winning):
    return len(set(have) & set(winning))


def score(line):
    _, winning, have = parse(line)
    n = winners(winning, have)
    return 2 ** (n - 1) if n >= 1 else 0


def parse(line):
    left_card_id, right_nums = [x.strip() for x in line.split(":")]
    card_id = elf.septoi(left_card_id)[1]
    winning, have = [elf.septoi(x.strip()) for x in right_nums.split("|")]
    return card_id, winning, have


def part2(lines):
    res = {}  # card-id: # of cards fully generated
    for line in reversed(lines): # building bottom-up
        card_id, winning, have = parse(line)
        n = winners(have, winning)
        copies = sum(res[copy_id] for copy_id in range(card_id + 1, card_id + 1 + n))
        res[card_id] = copies + 1  # plus original
    return sum(res.values())


if __name__ == '__main__':
    main()
