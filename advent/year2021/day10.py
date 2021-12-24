import collections

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


def part1(lines):
    total = 0
    for line in lines:
        invalid, _ = find_invalid(line)
        total += score(invalid)
    return total


def find_invalid(line):
    opens = "([{<"
    closes = ")]}>"
    open_stack = []
    counts = collections.Counter()
    for c in line:
        if c in opens:
            open_stack.append(c)
            counts[c] += 1
        if c in closes:
            if len(open_stack) == 0:
                return c, open_stack
            matching_open = opens[closes.find(c)]
            if open_stack[-1] != matching_open or counts[matching_open] <= 0:
                return c, open_stack
            else:
                open_stack.pop()
                counts[matching_open] -= 1
    return None, open_stack


def score(invalid):
    if not invalid:
        return 0
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return scores[invalid]


def part2(lines):
    scores = []
    for line in lines:
        invalid, open_stack = find_invalid(line)
        if not invalid:
            scores.append(score_completion(open_stack))
    return sorted(scores)[len(scores) // 2]


def score_completion(open_stack):
    """
    ): 1 point.
]: 2 points.
}: 3 points.
>: 4 points.
    """
    points = "0([{<"
    score = 0
    for c in open_stack[::-1]:
        score *= 5
        score += points.find(c)
    return score


if __name__ == '__main__':
    main()
