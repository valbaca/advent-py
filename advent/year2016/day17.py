from collections import namedtuple
from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop

from advent import elf


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))

    # lines = elf.read_lines(__file__)
    print("Part 1:", part1("veumntbg"))
    print("Part 2:", part2("veumntbg"))


# Loc = namedtuple('Loc', 'x y path')


@lru_cache(maxsize=2 ** 16)
def md5cached(s):
    return elf.md5(s)


@dataclass(slots=True, order=True)
class Loc:
    x: int
    y: int
    path: str

    def is_finished(self):
        return self.x == 3 and self.y == 3

    def next_steps(self, passcode):
        s = passcode + self.path
        steps = []
        up, down, left, right = md5cached(s)[0:4]
        if self.y != 0 and is_open(up):
            steps.append(Loc(self.x, self.y - 1, self.path + "U"))
        if self.y != 3 and is_open(down):
            steps.append(Loc(self.x, self.y + 1, self.path + "D"))
        if self.x != 0 and is_open(left):
            steps.append(Loc(self.x - 1, self.y, self.path + "L"))
        if self.x != 3 and is_open(right):
            steps.append(Loc(self.x + 1, self.y, self.path + "R"))
        return steps

def is_open(c):
    return c in "bcdef"

def part1(passcode, invert=False):
    ans = None
    q = [(0, Loc(0, 0, ""))]
    while q:
        _, loc = heappop(q)
        if loc.is_finished():
            if ans is None:
                ans = loc.path
            else:
                ans = loc.path if (len(loc.path) < len(ans)) != invert else ans
        else:  # not finished
            for next_step in loc.next_steps(passcode):
                priority = len(next_step.path) * (-1 if invert else 1)
                heappush(q, (priority, next_step))
    return ans

def part2(passcode):
    return len(part1(passcode, invert=True))


if __name__ == '__main__':
    main()
