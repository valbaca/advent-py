import re
from collections import Counter

from advent import elf

"""
Honestly got lucky that the "solving" was actually simple. I was worried it would involve 3SAT or some such.
A greedy approach ended up working.
I did a queue-based update model, though that might've been overkill

Counter was really handy for part 1
Really glad I built the 'data' object the way I did, it made part 2 trivial.
"""


def parse_line(line):
    splits = re.split(r"[\s(),]", line)
    strs = [s for s in splits if s != '']
    if "contains" not in strs:
        return strs, []
    sep = strs.index("contains")
    return strs[:sep], strs[sep + 1:]


def solve_known(data, allergen):
    updated_algs = [allergen]
    while updated_algs:
        alg = updated_algs.pop()
        if len(data['possible'][alg]) == 1:
            ing = list(data['possible'][alg])[0]
            data['known'][alg] = ing
            for k, v in data['possible'].items():
                if ing in v:
                    v.remove(ing)
                    updated_algs.append(k)


def update_data(data, ingredients, allergens):
    for ing in ingredients:
        data['ingredients'][ing] += 1
    unsolved_ings = set([ing for ing in ingredients if ing not in data['known']])
    for alg in allergens:
        if alg not in data['allergens']:
            data['allergens'].add(alg)
            data['possible'][alg] = unsolved_ings
        elif alg not in data['known']:
            data['possible'][alg] = data['possible'][alg] & unsolved_ings
        solve_known(data, alg)


def get_data(lines):
    ia_groups = [parse_line(line) for line in lines]
    data = {
        'ingredients': Counter(),
        'allergens': set(),
        'possible': {},  # allergen: set() of possible strings
        'known': {}  # allergen <-> ingredients
    }
    for ingredients, allergens in ia_groups:
        update_data(data, ingredients, allergens)
    return data


def part1(lines):
    data = get_data(lines)
    return len([ing for ing in data['ingredients'].elements() if ing not in data['known'].values()])


def part2(lines):
    data = get_data(lines)
    return ','.join([item[1] for item in sorted(data['known'].items())])


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
