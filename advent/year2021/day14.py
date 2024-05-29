import collections
import functools
import itertools

from advent import elf

"""
TIL: I forgot my filereader strips out blank lines! Wasted so much time on that.
Remember to use the debugger when nothing makes sense lol

itertools.pairwise is a welcome addition. This fn is needed ALL the time in puzzles.

Counter has 'most_common'! returns a sorted list of tuples, (elem, count)

Part 2:

This was a really interesting one. The part2 really required a whole different approach because the first
simply doesn't scale. The fact that N was less than 100 suggested a recursive approach was necessary.
Then the insight that the strings can basically be ignored once they're fully expanded and counted.

When I initially threw @cache on the recur function I was getting weird, incorrect results. The result
would change based on the size of the cache. HMMMM. 

My first thought was that the cache was holding refs to the returned Count collections and they were
getting updated. Tossing in .copy() didn't improve anything.

I then thought it was because I was using a global RLZ variable to hold the rules. Tried changing that to be 
passed in, but because the rules are a defaultdict, which isn't hashable, it doesnt work with @cache.

Then I realized that it was a different "global" variable! The memoize cache itself! The same function
was being used for the test run and the real code, so the real code runs of recur were re-using the 
results from the test run! Simply needed to move the recur function inside to have it be scoped to each
run. This also allows a closure over rlz, which also solves the global RLZ problem.

tl;dr: @cache saves the day again, but watch the cache reuse between runs! and use closures to get around the hash restriction
"""


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


def parse(lines):
    rlz = collections.defaultdict(dict)
    for line in lines[1:]:
        a, b, *_, c = line
        rlz[a][b] = c
    return lines[0], rlz


def apply_rules(s, rlz):
    out = ""
    for a, b in itertools.pairwise(s[:]):
        out += a
        if rlz[a].get(b):
            out += rlz[a][b]
    return out + s[-1]


def calc_diff(s):
    counts = collections.Counter(s[:]).most_common()
    return counts[0][1] - counts[-1][1]  # max - min


def part1(lines):
    s, rlz = parse(lines)  # rlz = pair insertion rules
    for _ in range(10):
        s = apply_rules(s, rlz)
    return calc_diff(s)


def part2(lines):
    start, rlz = parse(lines)  # rlz = pair insertion rules

    @functools.cache
    def recur(s, n):
        if n == 0:
            return collections.Counter(s[:-1])
        counter = collections.Counter()
        for a, b in itertools.pairwise(s):
            if rlz[a].get(b):
                counter.update(recur(f"{a}{rlz[a][b]}{b}", n - 1))
            else:
                counter[a] += 1  # counter.update(recur(a + b, rlz, n-1))
        return counter

    counts = recur(start, 40)
    counts[start[-1]] += 1
    comms = counts.most_common()
    return comms[0][1] - comms[-1][1]  # max_count - min_count


if __name__ == '__main__':
    main()
