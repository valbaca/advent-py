import elf


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
    def is_invalid(s):
        return len(s)%2 ==0 and s[:len(s)//2] == s[len(s)//2:]
    ranges = lines[0].split(",")
    total = 0
    for r in ranges:
        # print(r)
        a, b = [int(s) for s in r.split("-")]
        for x in range(a, b+1):
            if is_invalid(str(x)):
                total += x
    return total


def part2(lines):
    def is_invalid(s):
        divisors = (x for x in range(1, len(s)) if len(s) % x == 0)
        for d in divisors:
            quotient = len(s) // d
            prefix = s[:d]
            for i in range(1, quotient):
                # old c-style array traversal...
                part_start, part_end = (d*i), d*(i+1)
                part = s[part_start:part_end]
                if prefix != part:
                    break
            else: # rare adequate use of for-else
                return True
        return False

    ranges = lines[0].split(",")
    total = 0
    for r in ranges:
        # print(r)
        a, b = [int(s) for s in r.split("-")]
        for x in range(a, b+1):
            if is_invalid(str(x)):
                # print(x)
                total += x
    return total


if __name__ == '__main__':
    main()
