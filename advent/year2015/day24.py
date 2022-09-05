import itertools
import math
from advent.elf import product, read_lines, safe_atoi

def part1(input):
    ns = [safe_atoi(line) for line in input]
    return solve(ns, 3)

def solve(ints, slots):
    target = sum(ints) // slots
    maxN = len(ints) - 2
    minPkgs = math.inf
    ent = 0
    for i in range(1, maxN):
        if minPkgs <= i:
            return minPkgs, ent
        minPkgs, ent = combs(ints, i, target, minPkgs, ent)
    return minPkgs, ent

def combs(ints, i, target, minPkgs, ent):
    for viable in viable_combs(ints, i, target):
        if len(viable) < minPkgs:
            minPkgs, ent = len(viable), product(viable)
        elif len(viable) == minPkgs:
            viable_ent = product(viable)
            if viable_ent < ent:
                ent = viable_ent
    return minPkgs, ent

def viable_combs(ints, i, target):
    return [c for c in itertools.combinations(ints, i) if sum(c) == target]

def part2(input):
    ns = [safe_atoi(line) for line in input]
    return solve(ns, 4)

if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
