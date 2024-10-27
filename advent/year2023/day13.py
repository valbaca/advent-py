import numpy as np

from advent import elf

'''
TIL: this was a tricky one. lots of off-by-one errors.

This is also the first one that I really did solely in a Jupyter Notebook
and then copied over once I got it working.

Also learned the way to compare rows and cols in numpy:
- rows: a[r] == a[r2]
- cols: a[:, c] == a[:, c2]
which returns a numpy array of Booleans

Also the first time using the `else:` block with a `for` loop.
It was handy to have that way to break out while also handling the "success" case.

Finally, realized it was cleaner to range(1,end) and look back one (r-1) or (c-1) 
rather than the typical range(end-1) and look "forward" with (r+1) or (c+1) 
'''


def main():
    test_groups = elf.lines_blank_grouped(elf.test_file(__file__))
    groups = elf.lines_blank_grouped(elf.in_file(__file__))
    print("Part 1 (test):")
    print(part1(test_groups))
    print("Part 1:")
    print(part1(groups))
    print("Part 2 (test):")
    print(part2(test_groups))
    print("Part 2:")
    print(part2(groups))


def part1(groups):
    grids = [np.array([list(t) for t in tg]) for tg in groups]
    return sum(find_flip(g) for g in grids)


def find_flip(npg: np.array):
    rows, cols = npg.shape

    for r in range(1, rows):
        short = min(r, rows - r)
        if all(np.array_equal(npg[r - x - 1], npg[r + x]) for x in range(0, short)):
            return r * 100

    for c in range(1, cols):
        short = min(c, cols - c)
        if all(np.array_equal(npg[:, c - x - 1], npg[:, c + x]) for x in range(0, short)):
            return c


def part2(groups):
    grids = [np.array([list(t) for t in tg]) for tg in groups]
    return sum(find_flip_with_smudge(g) for g in grids)


def find_flip_with_smudge(npg: np.array):
    rows, cols = npg.shape

    for r in range(1, rows):
        short = min(r, rows - r)
        smudge = 1
        for x in range(0, short):
            eqs = npg[r - 1 - x] == npg[r + x]
            mismatches = (eqs == False).sum()
            if mismatches > 1:
                break
            if mismatches == 1:
                if smudge == 1:
                    smudge = 0
                else:
                    break
        else:  # if we didn't break out of the loop...
            if smudge == 0:
                return r * 100

    for c in range(1, cols):
        short = min(c, cols - c)
        smudge = 1
        for x in range(0, short):
            eqs = npg[:, c - x - 1] == npg[:, c + x]
            mismatches = (eqs == False).sum()
            if mismatches > 1:
                break
            if mismatches == 1:
                if smudge == 1:
                    smudge = 0
                else:
                    break
        else:  # if we didn't break out of the loop...
            if smudge == 0:
                return c


if __name__ == '__main__':
    main()
