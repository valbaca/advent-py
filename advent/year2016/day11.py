import math
import time
from dataclasses import dataclass
from functools import cached_property


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
LAST_FLOOR = FLOORS - 1
names = {
    0: 'Po',  # polonium
    1: 'Tm',
    2: 'Pm',  # promethium
    3: 'R',
    4: 'C',
    5: 'E',  # elerium
    6: 'D',  # dilithium
}


@dataclass(unsafe_hash=True, frozen=True)
class Building:
    steps: int
    elev: int
    gens: tuple  # maps generators to the floor its on; optimizing for size
    mics: tuple

    def solved(self):
        if self.elev != LAST_FLOOR:
            return False
        for gen_floor in self.gens:
            if gen_floor != LAST_FLOOR:
                return False
        for mic_floor in self.mics:
            if mic_floor != LAST_FLOOR:
                return False
        return True

    def safe(self):
        gens_by_floor, mics_by_floor = self.by_floor()
        for fn in range(FLOORS):
            chips = mics_by_floor[fn]
            if not chips:
                continue
            gens = gens_by_floor[fn]
            if not gens:
                continue
            if len(set(chips) - set(gens)) > 0:
                return False
        return True

    def floor_safe(self, floor):
        chips = set(mic_id for mic_id, mic_floor in enumerate(self.mics) if mic_floor == floor)
        if not chips:
            return True
        gens = set(gen_id for gen_id, gen_floor in enumerate(self.gens) if gen_floor == floor)
        if not gens:
            return True
        return len(chips - gens) == 0

    def move(self, dst, *items):
        if not (0 <= dst < FLOORS):
            return None
        new_gens = list(self.gens)
        new_mics = list(self.mics)
        for item_type, item_name in items:
            if item_type == 'G':
                new_gens[item_name] = dst
            else:
                new_mics[item_name] = dst

        moved = Building(
            steps=self.steps + 1,
            elev=dst,
            gens=tuple(new_gens),
            mics=tuple(new_mics)
        )
        if not moved.safe():
            return None
        return moved

    def generate_options(self):
        options = []
        gens_by_floor, mics_by_floor = self.on_floor(self.elev)
        go_below = False  # avoid moving items down a floor unless necessary
        if 0 < self.elev:
            gens_below, mics_below = self.on_floor(self.elev - 1)
            go_below = len(gens_below) + len(mics_below) > 0
        moves = [('G', gen_id) for gen_id in gens_by_floor] + [('M', mic_id) for mic_id in mics_by_floor]
        for move in moves:

            for second_move in moves[:]:
                if move == second_move:
                    continue
                options.append(self.move(self.elev + 1, move, second_move))
                # options.append(self.move(self.elev - 1, move, second_move)) # SKIP! Optimization
            # options.append(self.move(self.elev + 1, move)) # SKIP! Optimization
            if go_below:
                options.append(self.move(self.elev - 1, move))

        return (option for option in options if option is not None)

    @cached_property
    def score(self):
        total = 0
        for gen_floor in self.gens:
            total += (3 << gen_floor)
        for mic_floor in self.mics:
            total += (2 << mic_floor)
        return -total

    def __lt__(self, other):
        if self.steps < other.steps:
            return True
        elif self.steps > other.steps:
            return False
        else:
            our_score, other_score = self.score, other.score
            if our_score < other_score:
                return True
            elif our_score > other_score:
                return False
            else:
                return False  # tiebreaker?

    def by_floor(self):
        gens_by_floor, mics_by_floor = [[] for _ in range(FLOORS)], [[] for _ in range(FLOORS)]
        for gen_id, floor in enumerate(self.gens):
            gens_by_floor[floor].append(gen_id)
        for mic_id, floor in enumerate(self.mics):
            mics_by_floor[floor].append(mic_id)
        return gens_by_floor, mics_by_floor

    def on_floor(self, floor_num):
        """Returns set(gens), set(mics) where the floor matches the given floor"""
        return set(gen_id for gen_id, floor in enumerate(self.gens) if floor == floor_num), set(
            mic_id for mic_id, floor in enumerate(self.mics) if floor == floor_num),

    def __str__(self):
        s = []
        gens_by_floor, mics_by_floor = self.by_floor()
        for floor in range(FLOORS):
            floor_str = (" ".join([str(names[gen]) + "G" for gen in gens_by_floor[floor]])
                         + " ".join([str(names[mic]) + "M" for mic in mics_by_floor[floor]]))
            s.append(f"F{floor + 1} {'E' if self.elev == floor else '.'} {floor_str}")
        s.append(f"{self.steps=} {self.score=}")
        return "\n".join(reversed(s))


class RadixQueue:
    """Rather than using a heap, using a list where the index is the # of steps a building takes.
    This ensures we're working on the fastest solutions and can pull the next immediately"""
    def __init__(self):
        self.queue = [[]]
        self.last_pop = 0

    def first_with_item(self):
        for idx, arr in enumerate(self.queue):
            if len(arr) > 0:
                if idx != self.last_pop:
                    self.last_pop = idx
                return idx, arr
        return None, None

    def is_empty(self):
        if self.first_with_item() == (None, None):
            return True

    def push_all(self, index, items):
        while len(self.queue) <= index:
            self.queue.append([])
        self.queue[index].extend(items)

    def pop(self):
        _, arr = self.first_with_item()
        return arr.pop()


def runner(init):
    queue = RadixQueue()
    queue.push_all(init.steps, [init])
    seen = {init}
    min_steps = math.inf
    while not queue.is_empty():
        b = queue.pop()
        if min_steps <= b.steps:
            continue
        if b.solved():
            min_steps = b.steps
            # print(f"New min!: {min_steps}")
            continue
        options = b.generate_options()
        unseen = set(options) - seen
        seen.update(unseen)
        queue.push_all(b.steps + 1, unseen)
    return min_steps


def part1(test):
    b = None
    if test:
        # b.floors[0] = {('hydrogen', 'M'), ('lithium', 'M')}  # M = microchip
        # b.floors[1] = {('hydrogen', 'G')}  # G = Generator
        # b.floors[2] = {('lithium', 'G')}

        # b = Building(steps=0, elev=0, gens={
        #     'hydrogen': 1,
        #     'lithium': 2
        # }, mics={
        #     'hydrogen': 0,
        #     'lithium': 0,
        # })
        b = Building(steps=0, elev=0, gens=(1, 2), mics=(0, 0))
    else:
        # pass
        # b.floors[0] = {
        #     ('polonium', 'G'),
        #     ('thulium', 'G'),
        #     ('thulium', 'M'),
        #     ('promethium', 'G'),
        #     ('ruthenium', 'G'),
        #     ('ruthenium', 'M'),
        #     ('cobalt', 'G'),
        #     ('cobalt', 'M')
        # }
        # b.floors[1] = {
        #     ('polonium', 'M'),
        #     ('promethium', 'M'),
        # }

        b = Building(steps=0, elev=0, gens=(0, 0, 0, 0, 0), mics=(1, 0, 1, 0, 0))

    return runner(b)


def part2():
    b = Building(steps=0, elev=0, gens=(0, 0, 0, 0, 0, 0, 0), mics=(1, 0, 1, 0, 0, 0, 0))
    return runner(b)


if __name__ == '__main__':
    main()
