from advent import elf


def rem(a, i):
    rest, removed = a, []
    i1 = i + 1
    for _ in range(3):
        if i1 >= len(rest):
            # slow way
            ei = rest[i]
            i1 = i1 % len(rest)
            removed.append(rest[i1])
            del rest[i1]
            i = rest.index(ei)
            i1 = i + 1
        else:
            # fast way
            removed.append(rest[i1])
            del rest[i1]
        # i1 = (i+1) % len(rest)
        # e = a[(i + x) % len(a)]
        # removed.append(rest[i1])
        # del e[i1]
        # rest.remove(e)
    return rest, removed


def find_insert_pos(rest, curr):
    seek = curr - 1
    try:
        return rest.index(seek)
    except ValueError:
        # slow way
        mn = min(rest)
        while seek >= mn:
            if seek in rest:
                return rest.index(seek)
            seek -= 1
        mx = max(rest)
        return rest.index(mx)


def move(a, ci):
    curr = a[ci]
    rest, three = rem(a, ci)
    insert_pos = find_insert_pos(rest, curr)
    new_a = rest[:insert_pos + 1] + three + rest[insert_pos + 1:]
    new_ci = (new_a.index(curr) + 1) % len(new_a)
    return new_a, new_ci


def print_soln(a):
    a1 = a.index(1)
    a2 = a1 + 1 % len(a)
    ax = a[a2:] + a[:a1]
    return ''.join(map(str, ax))


def part1(inp, moves):
    a = list(map(elf.safe_atoi, inp))
    ci = 0
    for i in range(moves):
        a, ci = move(a, ci)
    return print_soln(a)
    # code here


def print_soln_p2(a):
    a1 = a.index(1)
    a2 = a1 + 1 % len(a)
    a3 = a2 + 1 % len(a)
    print(a2, a3)
    return a2 * a3


def part2(inp, moves):
    a = list(map(elf.safe_atoi, inp))
    for x in range(max(a) + 1, 1000000):
        a.append(x)
    ci = 0
    for i in range(moves):
        # print(i, end=" ")
        # print(f"ci={ci}, curr={a[ci]}, 1-index={a.index(1)} a={a[:100]}")
        a, ci = move(a, ci)
    print()
    return print_soln_p2(a)


def main():
    print(part1("974618352", 100))
    # print(part2("389125467", 10000000))
    # print(part2("974618352", 10000000))


if __name__ == '__main__':
    main()
