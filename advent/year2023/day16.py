from advent import elf

"""
Pretty easy one today. When brute-force is fast enough, it's great!
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


N = (-1, 0)
W = (0, -1)
E = (0, 1)
S = (1, 0)


def runner(g, start):
    def loc_check(loc):
        if 0 <= loc[0] < len(g) and 0 <= loc[1] < len(g[0]):
            return loc
        return None

    def grid_at(loc):
        if loc_check(loc):
            return g[loc[0]][loc[1]]
        return None

    def hit(src, d):
        """Returns list of next (locations,dir)"""
        dst = src[0] + d[0], src[1] + d[1]
        dch = grid_at(dst)
        if not dch:
            return []
        if dch == '.':
            return [(dst, d)]
        elif dch == '|':
            if d == N or d == S:
                return [(dst, d)]
            else:  # W E
                return [(dst, N), (dst, S)]  # split
        elif dch == '-':
            if d == N or d == S:
                return [(dst, W), (dst, E)]  # split
            else:
                return [(dst, d)]
        elif dch == '/':
            next_d = {N: E, W: S, E: N, S: W}
            return [(dst, next_d[d])]
        elif dch == '\\':
            next_d = {N: W, W: N, E: S, S: E}
            return [(dst, next_d[d])]

    q = [start]
    seen = set()
    while q:
        cur, d = q.pop(0)
        for hit_list in hit(cur, d):
            if hit_list not in seen:
                seen.add(hit_list)
                q.append(hit_list)
    return len(set(pos for pos, d in seen))


def part1(lines):
    g = [list(row) for row in lines]
    return runner(g, ((0, -1), E))


def part2(lines):
    g = [list(row) for row in lines]
    ans = 0
    for r in range(0, len(g)):
        ans = max(ans, runner(g, ((r, -1), E))) # left edge ->
        ans = max(ans, runner(g, ((r, len(g[0])), W))) # right edge <-
    for c in range(0, len(g[0])):
        ans = max(ans, runner(g, ((-1, c), S))) # top edge v
        ans = max(ans, runner(g, ((len(g), c), N))) # bottom edge ^
    return ans


if __name__ == '__main__':
    main()
