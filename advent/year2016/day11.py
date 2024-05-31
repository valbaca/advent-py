import heapq
import math
import time
from dataclasses import dataclass
from functools import cached_property

"""
FINALLY got this to run in less than a second.
Few key things (or really one major thing in multiple expressions):
PRUNE the potential space!

This is done in several ways:
1. Make the representation hashable, so it can be put into a set. This is done by making Building just (int, post) where
pos is a tuple (containing tuple pairs of where the generator and microchip are)
2. Using that, we can also easily represent the "functionally equivalent" states. It turns out the elements are a red-
herring; the names don't matter. So ((0,2), (1,2)) == ((1,2), (0,2)). This allows us to "normalize" the states by simply
sorting the position tuple, so ((1,2), (0,2)) becomes ((0,2), (1,2)) and now the set is even more useful!
3. Finally, avoid poor "steps". As in avoid moving just one thing up a floor when you could move two or moving two 
things down, or moving *anything* down if it's unnecessary.

#1 above is the most important, as it enables the rest.

I went through several different ways to represent the data:
- List of lists representing the floors and what was on the floor
- List of enum sets representing the floors and what was on the floor
- Two sets (generators and microchips) for where they were
- Finally landing on the tuple/list of generator-microchip floor location pairs

This is all what makes Advent of Code great.
You find that the straightforward way of representing the problem in code (e.g. list of floors) makes finding the soln
difficult. So you refactor and rearrange and invert and flip the data structures around.

These can be solved in any language but Python is especially well suited for completely changing the representation easily

The common refrain is "Python is slow" and while a Java equivalent would run faster, GETTING there in Python IS FASTER. 
"""


def main():
    print("Part 1 (test):", part1(test=True))

    start_time = time.time()
    print("Part 1:", part1(test=False))
    end_time = time.time()
    print(f"Took {end_time - start_time:.2f}s")

    start_time = time.time()
    print("Part 2:", part2())
    end_time = time.time()
    print(f"Took {end_time - start_time:.2f}s")


FLOORS = 4
TOP_FLOOR = FLOORS - 1


def add_in(tupe, diff, idx1, idx2):
    """Updates "within" a tuple (returning a new tuple)"""
    lst = list(tupe)
    lst[idx1] = tuple(
        orig + diff if idx == idx2 else orig
        for idx, orig in enumerate(lst[idx1])
    )
    return tuple(lst)


@dataclass(unsafe_hash=True, frozen=True)
class Building:
    elev: int
    pos: tuple  # ((<gen1 position>, <chip1 position>), etc)

    def normalize(self):
        return Building(self.elev, tuple(sorted(self.pos)))

    def solved(self):
        if self.elev != TOP_FLOOR:
            return False
        for gen_f, mic_f in self.pos:
            if gen_f != TOP_FLOOR or mic_f != TOP_FLOOR:
                return False
        return True

    def safe(self):
        gens_by_floor, mics_by_floor = self.by_floor()
        for fn in range(FLOORS):
            mics = mics_by_floor[fn]
            if not mics:
                continue
            gens = gens_by_floor[fn]
            if not gens:
                continue
            if len(mics - gens) > 0:
                return False
        return True

    def generate_options(self, seen):
        options = []
        go_above = self.elev < TOP_FLOOR
        go_below = self.elev > 0 and any(
            gen_pos == self.elev - 1 or mic_pos == self.elev - 1 for gen_pos, mic_pos in self.pos)

        poss = []  # possibilities
        for idx, (gen_pos, mic_pos) in enumerate(self.pos):
            if gen_pos == self.elev:
                poss.append((idx, 0))
            if mic_pos == self.elev:
                poss.append((idx, 1))
        for poss_idx, (idx, gen_or_mic) in enumerate(poss):
            if go_above:
                mut_pos = add_in(self.pos, 1, idx, gen_or_mic)
                options.append(Building(self.elev + 1, mut_pos))
                if poss_idx != len(poss) - 1:
                    for sec_idx, sec_gen_or_mic in poss[poss_idx + 1:]:
                        inner_pos = add_in(mut_pos, 1, sec_idx, sec_gen_or_mic)
                        options.append(Building(self.elev + 1, inner_pos))
            if go_below:
                options.append(Building(self.elev - 1, add_in(self.pos, -1, idx, gen_or_mic)))

        return set(option.normalize() for option in options if option.safe()) - seen

    def by_floor(self):
        gens_by_floor, mics_by_floor = [set() for _ in range(FLOORS)], [set() for _ in range(FLOORS)]
        for idx, (gen_f, mic_f) in enumerate(self.pos):
            gens_by_floor[gen_f].add(idx)
            mics_by_floor[mic_f].add(idx)
        return gens_by_floor, mics_by_floor

    @cached_property
    def score(self):
        return -1 * sum([self.elev + sum(a + b for a, b in self.pos)])

    def __lt__(self, other):
        return self.score < other.score


def runner(init):
    init = init.normalize()
    queue = [(0, init)]
    seen = {init}
    min_steps = math.inf
    while queue:
        idx, b = heapq.heappop(queue)
        if min_steps <= idx:
            continue
        if b.solved():
            min_steps = idx
            # print(f"New min!: {min_steps}")
            continue
        options = b.generate_options(seen)
        seen.update(options)
        queue.extend((idx + 1, option) for option in options)
        heapq.heapify(queue)
    return min_steps


def part1(test):
    if test:
        b = Building(elev=0, pos=(
            (1, 0),
            (2, 0)
        ))
    else:
        b = Building(elev=0, pos=(
            (0, 1),
            (0, 0),
            (0, 1),
            (0, 0),
            (0, 0)
        ))

    return runner(b)


def part2():
    b = Building(elev=0, pos=(
        (0, 1),
        (0, 0),
        (0, 1),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
    ))
    return runner(b)


if __name__ == '__main__':
    main()
