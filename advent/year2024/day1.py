from collections import Counter

from advent import elf

'''
I'm using a new keyboard (ZSA Moonlander MK1) and it's taking some major getting used to
 
So I'm just going with what works at the moment and requires as little typing or editing/refactoring as possible'''


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
    alist, blist = [],[]
    for line in lines:
        a,b = elf.septoi(line)
        alist.append(a)
        blist.append(b)
    alist.sort()
    blist.sort()

    return sum(abs(a-b) for a,b in zip(alist, blist))


def part2(lines):
    alist, blist = [],[]
    for line in lines:
        a,b = elf.septoi(line)
        alist.append(a)
        blist.append(b)
    c = Counter(blist)
    return sum(a * c[a] for a in alist)


if __name__ == '__main__':
    main()
