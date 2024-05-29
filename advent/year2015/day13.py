from collections import defaultdict
from itertools import permutations

from advent.elf import read_lines, septoi


def parse_happy(input):
    happy = defaultdict(dict)
    for line in input:
        seps = septoi(line)
        sign = -1 if seps[2] == "lose" else 1
        happy[seps[0]][seps[-1]] = sign * seps[3]
    return happy


def calc_happy(happy, guests):
    n = 0
    for i, g in enumerate(guests):
        hg = happy[g]  # type: dict
        left, right = hg.get(guests[i - 1], 0), hg.get(guests[(i + 1) % len(guests)], 0)
        n += left + right
    return n


def part1(input):
    happy = parse_happy(input)
    guest_list = list(happy.keys())
    mx = 0
    for guests in permutations(guest_list):
        mx = max(mx, calc_happy(happy, guests))
    return mx


def part2(input):
    happy = parse_happy(input)
    guest_list = list(happy.keys())
    guest_list.append("ME!")
    mx = 0
    for guests in permutations(guest_list):
        mx = max(mx, calc_happy(happy, guests))
    return mx


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
