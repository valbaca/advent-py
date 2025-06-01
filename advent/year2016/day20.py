from advent import elf
import intervaltree as it
# TIL: interval trees: I knew they existed but hadn't found or used this library

def main():
    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))

def parse(lines):
    pairs = [tuple(elf.septoi(line, '-')) for line in lines]
    pairs = [(a, b+1) for (a,b) in pairs]
    t = it.IntervalTree.from_tuples(pairs)
    t.merge_overlaps()
    return t

def part1(lines):
    t = parse(lines)
    for i in sorted(list(t)):
        if len(t[i.end]) == 0:
            return i.end
    return None

def part2(lines):
    t = parse(lines)
    full = it.IntervalTree.from_tuples([(0,4294967295+1)])
    for i in sorted(list(t)):
        full.chop(i.begin, i.end)
    full.merge_overlaps()
    return len(full)

if __name__ == '__main__':
    main()
