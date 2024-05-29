from yaml import safe_load

from advent.elf import read_lines, septoi

# perfect that this just so happens to be yaml
known_str = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""


def line_to_aunt(line):
    _, id, *props = septoi(line)  # sep[0] is name, seps[1] is id, rest are properties
    return id, dict(zip(props[0::2], props[1::2]))


def part1(input):
    known = safe_load(known_str)
    for line in input:
        id, aunt = line_to_aunt(line)
        if all([known.get(k) == v for k, v in aunt.items()]):
            return id


def part2(input):
    known = safe_load(known_str)
    for line in input:
        id, aunt = line_to_aunt(line)
        if all([matches(k, known.get(k), v) for k, v in aunt.items()]):
            return id


def matches(key, known_val, aunt_val):
    if key in ["cats", "trees"]:
        return aunt_val > known_val
    if key in ["pomeranians", "goldfish"]:
        return aunt_val < known_val
    return known_val == aunt_val


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
