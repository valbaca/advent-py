from functools import cache

from advent import elf
from advent.elf import septoi

# TIL: cache!!! This one was a doozy. Took all day (plus spent the day fighting with Python environments...
# first attempt used a bitset, way too slow going through all possible combinations
# looked at some hints which suggested Dynamic Programming (DP) which set me on a good path
# first solve for part 2 ran slow but in minutes. Turning off the lru_cache limit and replacing with @cache made it
# run instantly! More time was spent cleaning up the cache than doing work!

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


@cache
def rtl(springs, counts):
    '''
    springs: left string, like '???.###'
    counts: right string, as a tuple of numbers, like (1,1,3)

    This 'eats' right to left, starting with the right most count, say 3, and 'eats' from the right
    of springs, calling itself recursively: Example:
    1. rlt("???.###", (1,1,3)) => rtl("???.", (1,1)) => rtl("?", (1,)) => 1
    '''

    # base cases
    if not counts:
        return '#' not in springs # all '.' or '?' is basically empty once we're out of counts
    if not springs:
        return 0  # fail if springs is empty but we still have counts to match

    # eat up '.' and move the pointer to the right-most # or ?
    sp = len(springs) - 1
    while sp >= 0 and springs[sp] == '.':
        sp -= 1
    if sp < 0:
        return 0 # string was all '.', fail

    subsprings = springs[:sp + 1]

    if subsprings[-1] == '?':
        # branch at the "right-beginning" of a spring
        return rtl(subsprings[:-1] + '#', counts) + rtl(subsprings[:-1], counts)

    # then we start matching # and ? until we've reduced the right-most count
    curr_count = counts[-1]

    while curr_count != 0:
        if len(subsprings) > 0 and (subsprings[-1] == '#' or subsprings[-1] == '?'):
            # once we're "in" a subsequence, we don't need to branch; we can't!
            subsprings = subsprings[:-1]
            curr_count -= 1
        else:
            return 0  # subsequence hit a '.', fail
    if len(subsprings) != 0 and subsprings[-1] == '#':
        return 0  # subsequence kept going, fail
    else:
        return rtl(subsprings[:-1], counts[:-1])  # FINALLY, we had a good match


def part1(lines):
    total = 0
    for line in lines:
        springs, counts = [s.strip() for s in line.split(' ')]
        ans = rtl(springs, tuple(septoi(counts)))
        total += ans
    return total


def part2(lines):
    total = 0
    for line in lines:
        springs, counts = [s.strip() for s in line.split(' ')]
        exp_springs = "?".join([springs] * 5)
        exp_counts = ",".join([counts] * 5)
        ans = rtl(exp_springs, tuple(septoi(exp_counts)))
        total += ans
    return total


if __name__ == '__main__':
    main()
