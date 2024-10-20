import itertools

from advent import elf


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

def diffs(xs):
    return [b-a for (a,b) in itertools.pairwise(xs)]

def part1(lines):
    hists = [elf.septoi(line) for line in lines]
    def calc_next(xs):
        if len(set(xs)) == 1:
            return xs[0]
        return xs[-1] + calc_next(diffs(xs))
    return sum(calc_next(hist) for hist in hists)

def part2(lines):
    hists = [elf.septoi(line) for line in lines]
    def calc_prev(xs):
        if len(set(xs)) == 1:
            return xs[0]
        return xs[0] - calc_prev(diffs(xs))
    return sum(calc_prev(hist) for hist in hists)


if __name__ == '__main__':
    main()
