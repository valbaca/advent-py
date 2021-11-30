import functools

from advent import elf
from advent.util.Link import Link

"""
This is a really great Advent problem. Shows how a reasonable part 1 solution doesn't scale to part 2.
And it shows where linked lists are really useful! and situationally superior to (poor) array traversal.

I also didn't refactor Part 1 with the linked list used in part 2 out of laziness and to show the two approaches.
"""


def main():
    print("Part 1 (test):", part1(5))

    ans1 = part1(3004953)
    assert (ans1 == 1815603)
    print("Part 1:", ans1)

    print("Part 2:", part2(5))
    print("Part 2:", part2(3004953))


def gen_inc(n):
    return lambda x: (x + 1) % n


def gen_get_elf(elves, e, iterator):
    next_e = iterator(e)
    while elves[next_e] == 0:
        next_e = iterator(next_e)
    return next_e


def part1(n):
    elves = [i + 1 for i in range(n)]
    inc = gen_inc(n)
    get_next_elf = functools.partial(gen_get_elf, iterator=inc)
    e = 0
    while True:
        next_e = get_next_elf(elves, e)
        if e == next_e:
            return elves[e]  # last elf!
        elves[next_e] = 0  # steal
        e = get_next_elf(elves, next_e)


def part2(n):
    # Create the circle of elves via a Linked List
    e = Link(1)  # first elf
    last = e
    for i in range(2, n + 1):
        nxt = Link(i)
        last.next = nxt
        last = nxt
    last.next = e
    x = e  # x = across...a cross :P
    for _ in range((n // 2) - 1):
        # move x to be the elf *before* the elf across from e, for easy elf deletion
        x = x.next
    elves_remaining = n
    while elves_remaining > 1:
        # print(f"e {e.value} is deleting x.next {x.next.value} and x={x.value}")
        x.del_next()  # steal
        if elf.odd(elves_remaining):  # This if-check was the tricky bit
            x = x.next
        e = e.next
        elves_remaining -= 1
    return e.value


if __name__ == '__main__':
    main()
