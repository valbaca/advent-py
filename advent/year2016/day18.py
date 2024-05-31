import time


def main():
    lines = "^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^."
    print("Part 1:", part1(lines))
    start = time.time()
    print("Part 2:", part2(lines))
    end = time.time()
    print(f"{end - start:.2f}s")


def part1(lines):
    return safe_tiles(40, lines)


def safe_tiles(row, tiles):
    count = 0
    for _ in range(row):
        count += count_safe(tiles)
        tiles = next_line(tiles)
    return count


def count_safe(tiles):
    return tiles.count('.')


def next_line(prev):
    return "".join([determine(prev_subs(prev, i)) for i in range(len(prev))])


def determine(s):
    return '^' if s in {"^^.", ".^^", "^..", "..^"} else '.'


def prev_subs(prev, i):
    if i == 0:
        return "." + prev[:2]
    elif i == len(prev) - 1:
        return prev[i - 1:] + '.'
    return prev[i - 1:i + 2]


def part2(lines):
    return safe_tiles(400_000, lines)


if __name__ == '__main__':
    main()
