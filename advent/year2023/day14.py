import numpy as np

from advent import elf


'''
TIL: how to get a hashable/string representation of numpy array

This was another doozy. Part2 was one I was not able to figure out on my own, but got a small hint to detect a loop.

After that, had some trouble with figuring out the rotations (once counterclockwise, then the reset clockwise) as well
as figuring out caching the 2d numpy array.

Finally, figured out the loop by saving the cache-hits (which means they're a repeat) in a list.

Once the list has an even number (meaning a possible repeat), check it.
After that, it's some simple mod-math to figure out what it'll look like at ONE BILLION

Runs in ~5s
'''

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


def slide(a):
    lp = 0

    while lp < len(a):
        # move lp to first empty space
        while lp < len(a) - 1 and a[lp] != '.':
            lp += 1
        if lp == len(a) - 1:
            break  # end
        rp = lp + 1
        # find the next boulder
        while rp < len(a) - 1 and a[rp] == '.':
            rp += 1
        if a[rp] == '#' or a[rp] == '.':
            lp += 1
            continue
        a[lp], a[rp] = a[rp], a[lp]
        lp += 1
    return a


def score(a):
    return sum(len(a) - i for i, e in enumerate(a) if e == 'O')


def part1(lines):
    arr = np.array([list(l) for l in lines]).transpose()
    return sum(score(slide(row)) for row in arr)


NUM_CYCLES = 1000000000


def part2(lines):
    init_rot = 1
    cche = {}  # cache of array-hashes to the next-array that would be generated

    def score_arr(arr):
        return sum(score(row) for row in arr)

    # Mutates arr, so need to clone before calling this
    def inner_cycle(arr):
        for _ in range(4):
            for row in arr:
                slide(row)
            arr = np.rot90(arr, -1)  # clockwise rotation so "left" goes from N->W->S->E
        return arr

    a = np.array([list(l) for l in lines])
    a = np.rot90(a, init_rot)  # initial counter-clockwise rotation to have it be North == left/0 to match slide()
    seen = []  # stores running hashes and scores in order to detect a Loop
    for cy in range(NUM_CYCLES):
        a_hash = str(a.tobytes())
        if a_hash in cche:
            seen.append((a_hash, score_arr(a)))  # store tuple of hash (for uniqueness) and score (to get the answer)
            # Check for Loop
            if len(seen) % 2 == 0:
                mid = len(seen) // 2
                if all(x == y for x, y in zip(seen[:mid], seen[mid:])):  # first half == second half
                    # seen_str = "\n".join(str(s) for s in seen)
                    # print(f"LOOP! len={mid} ending@{cy} score={score_arr(arr)} {seen_str}")

                    # offset of when the cycle begins:  NUM_CYCLES - cy
                    # how long the cycle is: mid
                    # -1 for 0 index
                    # [1] to get the score, not the hash
                    return seen[((NUM_CYCLES - cy) % mid) - 1][1]
            a = cche[a_hash]
        else:  # cache miss
            seen = []  # reset
            cche[a_hash] = inner_cycle(a.copy())  # clone before we mutate!
            a = cche[a_hash]
    return score_arr(a)


if __name__ == '__main__':
    main()
