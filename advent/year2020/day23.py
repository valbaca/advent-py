from advent import elf

"""
This one was a great challenge.
I did end up having to look up hints for part 2, which really helped.
Like many, I started with a naive array-list implementation, but that did not scale to part 2.
I thought about using a circular linked-list, but was concerned about the runtime of finding the destination cup.

Then I rewrote the whole thing to use the `after` array, where given cup i, a[i] gives the cup after cup i.
The description of part 2 should've been an obvious hint that such an array would be a good approach.
When you have contiguous values, such a lookup array is perfect.
Other than that, a hash-table would've been good too.
"""


def move(a, c, mx):  # after_array, current, max
    ptr = a[c]
    removed = []
    for _ in range(3):
        removed.append(ptr)
        ptr = a[ptr]
    # stitch curr -> _ -> _ -> _ -> ptr to be curr -> ptr
    a[c] = ptr
    # find the destination cup
    dest = c - 1
    while dest in removed or dest == 0:
        if dest == 0:
            dest = mx
        if dest in removed:
            dest -= 1
    # insert removed between dest -> [removed] -> after_dest
    after_dest = a[dest]
    a[dest] = removed[0]
    a[removed[-1]] = after_dest
    return a[c]


def print_soln_p1(a):
    out = [1]
    while len(out) < (len(a) - 1):
        out.append(a[out[-1]])
    return ''.join(map(str, out[1:]))


def part1(inp, moves):
    print(f"Part 1: input={inp}, moves={moves}")
    inp_a = list(map(elf.safe_atoi, inp))
    after = [0 for _ in range(len(inp_a) + 1)]
    mx = inp_a[-1]
    for i in range(len(inp_a) - 1):
        val = inp_a[i]
        after[val] = inp_a[i + 1]
        if val > mx:
            mx = val
    after[inp_a[-1]] = inp_a[0]
    curr = inp_a[0]
    for _ in range(moves):
        curr = move(after, curr, mx)
    return print_soln_p1(after)


def print_soln_p2(after):
    a1 = after[1]
    a2 = after[a1]
    print(a1, a2)
    return a1 * a2


def part2(inp, moves):
    print(f"Part 2: input={inp}, moves={moves}")
    inp_a = list(map(elf.safe_atoi, inp))
    after = [0 for _ in range(1000001)]
    for i in range(len(inp_a) - 1):
        val = inp_a[i]
        after[val] = inp_a[i + 1]
    last = inp_a[-1]
    for i in range(max(inp_a), 1000000):
        after[last] = i + 1
        last = i + 1
    after[1000000] = inp_a[0]
    curr = inp_a[0]
    mx = 1000000
    for _ in range(moves):
        curr = move(after, curr, mx)
    return print_soln_p2(after)


def main():
    print(part1("389125467", 10))
    print(part1("389125467", 100))

    ans1 = part1("974618352", 100)
    assert (ans1 == "75893264")
    print(ans1)

    print(part2("389125467", 10000000))
    print(part2("974618352", 10000000))


if __name__ == '__main__':
    main()
