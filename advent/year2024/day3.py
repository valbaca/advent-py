from advent import elf

# This wasn't a pretty one.

# Small trick to this one was that in part 2 the 'enabled' flag persists across lines
# could've done this better but just slapped in a global variable

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


# This is clunky but going character by character makes sense to me
def parse_mul(line, i):
    c = line[i]
    if c != 'm':
        return
    # at m
    if line[i:i + 4] != "mul(":
        return
    p = i + 4  # moving pointer
    a = ""  # string, first number
    while p < len(line):
        if line[p].isdigit():
            if len(a) < 3:
                a += line[p]
            else:
                return
        elif line[p] == ',':
            if len(a) < 1:
                return
            a = int(a)
            p += 1 # move up
            break # break out of while True
        else:
            return
        p += 1
    b = ""

    while p < len(line):
        if line[p].isdigit():
            if len(b) < 3:
                b += line[p]
            else:
                return
        elif line[p] == ')':
            if len(b) < 1:
                return
            b = int(b)
            return a * b # WHOO!
        else:
            return
        p += 1


def p1(line):
    total = 0
    for i in range(len(line)):
        res = parse_mul(line, i)
        if res is not None:
            total += res
    return total



def part1(lines):
    return sum(p1(line) for line in lines)

enabled = True # gross...but it works

def p2(line):
    global enabled
    total = 0
    for i in range(len(line)):
        if line[i:].startswith('do()'):
            enabled = True
        elif line[i:].startswith("don't()"):
            enabled = False
        if enabled:
            res = parse_mul(line, i)
            if res is not None:
                total += res
    return total

def part2(lines):
    global enabled
    enabled = True
    return sum(p2(line) for line in lines)


if __name__ == '__main__':
    main()
