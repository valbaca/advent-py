from advent import elf


def rem(a, i):
    removed = []
    i1 = i + 1
    for _ in range(3):
        if i1 < len(a):
            removed.append(a[i1])
            del a[i1]
        else:
            removed.append(a[0])
            del a[0]
    return a, removed


def max_with_index(a):
    mx, mi = a[0], 0
    for i, e in enumerate(a):
        if e > mx:
            mx, mi = e, i
    return mx, mi


def find_dest(rest, three, curr):
    seek = curr - 1
    while seek in three:
        seek -= 1
    if seek < 1:
        return max_with_index(rest)[1]
    return rest.index(seek)


def move(a, ci):
    curr = a[ci]
    rest, three = rem(a, ci)
    dest1 = find_dest(rest, three, curr) + 1
    rest[dest1:dest1] = three
    if dest1 <= ci:
        new_ci = (rest.index(curr) + 1) % len(rest)
    else:
        new_ci = ci + 1
    return rest, new_ci


def print_soln_p1(a):
    a1 = a.index(1)
    a2 = a1 + 1 % len(a)
    ax = a[a2:] + a[:a1]
    return ''.join(map(str, ax))


def part1(inp, moves):
    a = list(map(elf.safe_atoi, inp))
    ci = 0
    for i in range(moves):
        a, ci = move(a, ci)
    return print_soln_p1(a)


def print_soln_p2(a):
    a1 = a.index(1)
    a2 = a1 + 1 % len(a)
    a3 = a2 + 1 % len(a)
    print(a2, a3)
    return a2 * a3


def part2(inp, moves):
    a = list(map(elf.safe_atoi, inp))
    for x in range(max(a) + 1, 1000001):
        a.append(x)
    ci = 0
    for i in range(moves):
        if i % 10000 == 0:
            print(f"move {i}")
        a, ci = move(a, ci)
    print()
    return print_soln_p2(a)


def main():
    ans1 = part1("974618352", 100)
    assert (ans1 == "75893264")
    print(ans1)
    print(part2("389125467", 10000000))
    print(part2("974618352", 10000000))


if __name__ == '__main__':
    main()
