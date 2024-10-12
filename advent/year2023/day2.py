from advent import elf

# TIL: easy one, but just keeping it straightforward
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


def score(line):
    bag = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    pre, suf = line.split(":")
    game_id = int(pre.split(" ")[1])

    for game_str in suf.split(";"):
        # "3 blue, 4 red;"...
        for reveal in (r.strip() for r in game_str.split(",")):
            num, color = reveal.split(" ")
            if int(num) > bag[color]:
                return 0
    return int(game_id)


def part1(lines):
    return sum(score(line) for line in lines)


def power_score(line):
    pre, suf = line.split(":")
    # game_id = int(pre.split(" ")[1])
    mins = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for game_str in suf.split(";"):
        # "3 blue, 4 red;"...
        for reveal in (r.strip() for r in game_str.split(",")):
            num_str, color = reveal.split(" ")
            num = int(num_str)
            if num > mins[color]:
                mins[color] = num
    return elf.product(mins.values())


def part2(lines):
    return sum(power_score(line) for line in lines)


if __name__ == '__main__':
    main()
