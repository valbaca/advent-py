from functools import cache
from advent import elf

# TIL: I must've seen this one before or something very similar. I knew exactly
# where part 2 was going and I knew that sorting the towels by largest would 
# be the best bet.
# I could've easily combined part 1 and 2 code, but keeping them separate to 
# show how little was changed

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
    towels = elf.septoi(lines[0])
    towels = tuple(sorted(towels, key=lambda k: -len(k)))

    @cache
    def possible(s: str):
        if not s:
            return True
        for t in towels:
            if s.startswith(t):
                is_possible = possible(s[len(t):])
                if is_possible:
                    return True
        return False

    total = 0
    for line in lines[1:]:
        if possible(line):
            total += 1
    return total

def part2(lines):
    towels = elf.septoi(lines[0])
    towels = tuple(sorted(towels, key=lambda k: -len(k)))

    @cache
    def possible(s: str):
        if not s:
            return 1
        count = 0
        for t in towels:
            if s.startswith(t):
                count += possible(s[len(t):])
        return count

    total = 0
    for line in lines[1:]:
        total += possible(line)
    return total


if __name__ == '__main__':
    main()
