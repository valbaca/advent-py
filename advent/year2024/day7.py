from itertools import product

from advent import elf
from advent.elf import septoi


# ez pz with itertools.product
# part2 runs a bit slow but gets there in a few seconds

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


def solvable(tgt, vals, ops=None):
    if ops is None:
        ops = ['*', '+']
    combinations = list(product(ops, repeat=len(vals)))
    for comb in combinations:
        curr = vals[0]
        for v, c in zip(vals[1:], comb):
            if c == '+':
                curr += v
            elif c == '*':
                curr *= v
            elif c == '|':
                curr = int(str(curr) + str(v))
        if tgt == curr:
            return True
    return False

def part1(lines):
    total = 0
    for line in lines:
        tgt, *vals = septoi(line)
        if solvable(tgt, vals):
            total += tgt
    return total

def part2(lines):
    total = 0
    for line in lines:
        tgt, *vals = septoi(line)
        if solvable(tgt, vals, ops=['*', '+', '|']):
            total += tgt
    return total


if __name__ == '__main__':
    main()
