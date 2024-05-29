from advent.elf import read_lines


def part1(input):
    return len(visit(input[0]))


def visit(s):
    seen = set()
    pos = (0, 0)
    seen.add(pos)
    for ch in s:
        x, y = pos
        if ch == "^":
            pos = (x, y - 1)
        elif ch == ">":
            pos = (x + 1, y)
        elif ch == "v":
            pos = (x, y + 1)
        elif ch == "<":
            pos = (x - 1, y)
        seen.add(pos)
    return seen


def part2(input):
    s = input[0]
    santa, robo = "".join(s[::2]), "".join(s[1::2])
    return len(visit("".join(santa)) | visit("".join(robo)))


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
