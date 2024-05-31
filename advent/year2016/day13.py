import heapq
from functools import lru_cache


def main():
    print("Part 1 (test):", part1_test())

    print("Part 1:", part1())
    print("Part 2:", part2())


@lru_cache
def is_wall(fav, x, y):
    sm = x * x + 3 * x + 2 * x * y + y + y * y + fav
    return int.bit_count(sm) % 2 != 0


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def runner(target, fav, max_steps=None):
    init = (1, 1)
    q = []
    heapq.heappush(q, (0, (distance(target, init), init)))
    seen = set()
    seen.add(init)

    def visit(steps, coor):
        x, y = coor
        if x < 0 or y < 0:
            return
        if coor in seen:
            return
        if is_wall(fav, x, y):
            return
        seen.add(coor)
        heapq.heappush(q, (steps, (distance(target, coor), coor)))

    while q:
        steps, (dist, coor) = heapq.heappop(q)
        if max_steps and steps >= max_steps:
            return len(seen)

        if coor == target:
            return steps
        visit(steps + 1, (coor[0] + 1, coor[1]))  # right
        visit(steps + 1, (coor[0], coor[1] + 1))  # down
        visit(steps + 1, (coor[0], coor[1] - 1))  # up
        visit(steps + 1, (coor[0] - 1, coor[1]))  # left


def part1_test():
    return runner((7, 4), 10)


def part1():
    return runner((31, 39), 1350)


def part2():
    return runner((999, 999), 1350, max_steps=50)


if __name__ == '__main__':
    main()
