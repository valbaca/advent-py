import re


def main():
    with open("day3.txt") as fin:
        lines = [line.strip() for line in fin]
        print(part1(lines))
        print(part2(lines))


def part1(lines):
    count = 0
    for line in lines:
        splits = re.split(r'\s+', line)
        ints = [int(s) for s in splits]
        if is_triangle(*ints):
            count += 1
    return count


def part2(lines):
    count = 0
    triangles = [[], [], []]
    for line in lines:
        splits = re.split(r'\s+', line)
        ints = [int(s) for s in splits]
        for i in range(3):
            triangles[i].append(ints[i])
        if len(triangles[0]) == 3:
            for triangle in triangles:
                if is_triangle(*triangle):
                    count += 1
            triangles = [[], [], []]
    return count


def is_triangle(a, b, c):
    return (a + b > c) and (a + c > b) and (b + c > a)


if __name__ == "__main__":
    main()
