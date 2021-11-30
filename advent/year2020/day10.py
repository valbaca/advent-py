import functools
import time

from advent import elf

"""
Part 1 was super easy, just sort.

Part 2 was taking wayyy too long to solve (as hinted by the question)

But caching/memoization (via @functools.lru_cache) saved the day!

I was using a depth-first search and realized once you get to a particular adapter, it's just repeating work.
After adding memoization, part 2 runs instantly!

Unfortunately, Python cannot has a list, so cannot use lru_cache on a method that has a list as an arg.
So to get around that, I first used a global variable JOLTS
Then as an improvement on that, I used a class with a jolts field.

I then simplified the method args further until I got down to just one!
"""


def main():
    lines = elf.read_lines(__file__, elf.safe_atoi)
    print(part1(lines))
    # part 2 was taking so long I added timing, but after lru_cache, takes <1ms
    tic = time.perf_counter()
    answer2 = part2(lines)
    toc = time.perf_counter()
    print(answer2)
    print(f"Part 2 {toc - tic:0.4f} seconds")


def lines_to_jolts(lines):
    jolts = lines.copy()
    jolts.append(0)
    jolts.sort()
    jolts.append(3 + max(jolts))
    return jolts


def part1(lines):
    jolts = lines_to_jolts(lines)
    diffs = []
    for i in range(1, len(jolts)):
        diffs.append(jolts[i] - jolts[i - 1])
    return diffs.count(1) * diffs.count(3)


class JoltSolver:
    def __init__(self, jolts):
        self.jolts = jolts

    @functools.lru_cache
    def solve(self, last):
        # last is the jolts value of the last-added adapter

        # Our device is exactly 3 Jolts higher that the highest (last) adapter in our bag
        # so that's all we need to check for a valid solution
        if last == self.jolts[-1]:
            return 1
        total = 0
        for jolt in self.jolts:
            diff = jolt - last
            if 0 < diff <= 3:
                total += self.solve(jolt)
            elif diff > 3:
                break
        return total


def part2(lines):
    jolts = lines.copy()
    jolts.sort()
    jolt_solver = JoltSolver(jolts)
    return jolt_solver.solve(0)


if __name__ == '__main__':
    main()
