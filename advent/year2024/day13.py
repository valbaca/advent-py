from advent import elf
from advent.elf import ad


# Yay! Linear algebra!
# wasted more time futzing with numpy and could've been done in an hour if I'd just written from scratch from the get go
# I did also add some Tuple helper functions
# Rather than a[0] + 1000, a[1] + 1000; can do ad(a, 1000)

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


def part1(lines):
    return same(lines)

def part2(lines):
    return same(lines, plus=10000000000000)

def same(lines, plus=0):
    # group into sets of 3
    groups = [lines[i:i + 3] for i in range(0, len(lines), 3)]
    total = 0
    for group in groups:
        a_line, b_line, prize_line = group
        ba = elf.only_ints(elf.septoi(a_line))
        bb = elf.only_ints(elf.septoi(b_line))
        prize = ad(elf.only_ints(elf.septoi(prize_line)), plus)
        tokens = algebra_solve(ba, bb, prize)
        total += tokens
    return total


def algebra_solve(ba, bb, prize):
    ax, ay = ba
    bx, by = bb
    px, py = prize
    a = (px * by - py * bx) // (by * ax - bx * ay)  # num of times a button is pressed
    b = (px * ay - py * ax) // (ay * bx - by * ax)  # num of times b button is pressed

    # check if it's a solution (will be if there was no remainder)
    x = ba[0] * a + bb[0] * b
    y = ba[1] * a + bb[1] * b
    if x == prize[0] and y == prize[1]:
        return a * 3 + b  # coins
    return 0


if __name__ == '__main__':
    main()
