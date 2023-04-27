from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2:")
    print(part2(lines))


def move_right(mx, r, c):
    next_c = (c + 1) % len(mx[r])
    return ((r, c), (r, next_c)) if mx[r][next_c] == '.' else None


def move_down(mx, r, c):
    next_r = (r + 1) % len(mx)
    return ((r, c), (next_r, c)) if mx[next_r][c] == '.' else None


def part1(lines):
    mx = [list(line) for line in lines]
    n = 1
    while True:
        moves_count = 0
        for sc in ">v":  # sea cucumbers
            moves = []
            for r, row in enumerate(mx):
                for c, ch in enumerate(row):
                    if ch == sc:
                        if ch == ">":
                            moves.append(move_right(mx, r, c))
                        else:
                            moves.append(move_down(mx, r, c))
            moves = [m for m in moves if m is not None]
            for src, dst in moves:
                r, c = src
                mx[r][c] = '.'
                r, c = dst
                mx[r][c] = sc
            moves_count += len(moves)
        if moves_count == 0:
            return n
        n += 1
        moves_count = 0


def part2(lines):
    return "MERRY CHRISTMAS!!! 🎄🎄🎄"


if __name__ == '__main__':
    main()
