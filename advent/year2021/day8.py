from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (single-test, expected=5353):")
    print(part2(["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    return sum([count_1478(line) for line in lines])


def count_1478(line):
    splits = line.split(" | ")[1].split(" ")
    return len([s for s in splits if len(s) in [2, 4, 3, 7]])


ORIG = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg"
]

LENS = [len(o) for o in ORIG]


def patterns():
    # Used this to help find the overlapping patterns
    for i, chars in enumerate(ORIG[:]):
        print(f"n={i} chars={chars} len={len(chars)}")
        for j, other_chars in enumerate(ORIG[:]):
            if len(other_chars) in [2, 4, 3, 7]:
                print(f"(j={j}, len(j)={len(other_chars)}, ovlap={len(set(chars) & set(other_chars))})")
        print()


def calc_output(line):
    signals, output = line.split(" | ")
    signals = signals.split(" ")
    output = output.split(" ")
    sigs = signals + output

    # The guaranteed numbers that are easy to deduce from
    # We use the set of chars and how those sets "overlap" (or intersect with &)
    # to deduce the other numbers
    # If we *had to* we could check the count of all the overlapping segments, but it's unnecessary.
    # Thankfully, each digit has some unique number of segments that overlap
    # with these "easy" ones to make it straightforward
    # c/o https://www.reddit.com/r/adventofcode/comments/rbj87a/comment/ho42bqj
    # but rewritten in a way that I better understand and can read it
    easy = {1: [set(s) for s in sigs if len(s) == len(ORIG[1])][0],
            4: [set(s) for s in sigs if len(s) == len(ORIG[4])][0],
            7: [set(s) for s in sigs if len(s) == len(ORIG[7])][0]}
    result = ""
    for outp in output:
        l = len(outp)
        if l == LENS[1]:
            result += "1"
        elif l == LENS[4]:
            result += "4"
        elif l == LENS[7]:
            result += "7"
        elif l == LENS[8]:
            result += "8"
        elif l == 5:
            # Value is either 2, 3, or 5
            #            1 4 7 (the easy nums)
            # 2 overlaps 1 2 2 (the count of 2 segments overlapping with 4 is unique)
            # 3 overlaps 2 3 3 (the count of 2 segments overlapping with 1 is unique)
            # 5 overlaps 1 3 2 (no unique, but can just put in else)
            outp_set = set(outp)
            if len(outp_set & easy[4]) == 2:
                result += "2"
            elif len(outp_set & easy[1]) == 2:
                result += "3"
            else:
                result += "5"
        elif l == 6:
            # Value is either 0, 6, or 9
            #            1 4 7 (the easy nums)
            # 0 overlaps 2 3 3 (no unique, put in else)
            # 6 overlaps 1 3 2 (the count of 1 segment overlapping with 1 is unique)
            # 9 overlaps 2 4 3 (the count of 4 segments overlapping with 4 is unique)
            outp_set = set(outp)
            if len(outp_set & easy[1]) == 1:
                result += "6"
            elif len(outp_set & easy[4]) == 4:
                result += "9"
            else:
                result += "0"
    return int(result)


def part2(lines):
    return sum([calc_output(line) for line in lines])


if __name__ == '__main__':
    main()
