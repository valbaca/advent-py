from math import log2

from advent import elf
from advent.elf import product

"""
Not exactly "challenging" other than understanding the instructions.
The "hex-to-binary" function was a tad tricky because there was an implicit
prefix padding expectation.
"""


def main():
    lines = elf.read_lines(__file__)
    print("Part 1:")
    print(part1(lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    bins = hex_to_bins(lines[0])
    return sum_vers(bins)[0]


def hex_to_bins(s):
    """Hex string to binary string representation, prefixes 0s as needed"""
    # This was the weirdest part, c/o https://stackoverflow.com/a/4859937/158886
    num_of_bits = int(len(s) * log2(16))
    return bin(int(s, 16))[2:].zfill(num_of_bits)


def bi(s):
    """Binary string to integer: btoi("100") -> 4"""
    return int(s, 2)


def sum_vers(s):
    """Returns version sum (for part 1), value (for part 2), and end (for parsing)"""
    ver, type = bi(s[0:3]), bi(s[3:6])
    if type == 4:
        val, end = parse_literal(s)
        return ver, val, end
    else:
        length = s[6]
        p = 7  # pointer within string
        sub_vals = []
        if length == '0':  # next 15 bits is length of subs
            length_sub = bi(s[p:p + 15])
            p += 15
            end_all_sub = p + length_sub
            while p < end_all_sub:
                sub_ver, sub_val, sub_end = sum_vers(s[p:])
                ver += sub_ver
                sub_vals.append(sub_val)
                p += sub_end
        else:  # '1' # next 11 bits are the number of subs
            num_subs = bi(s[p:p + 11])
            p += 11
            for _ in range(num_subs):
                sub_ver, sub_val, sub_end = sum_vers(s[p:])
                ver += sub_ver
                sub_vals.append(sub_val)
                p += sub_end
        val = evaluate(type, sub_vals)
        return ver, val, p


def parse_literal(s):
    """Returns literal's value (for part 2) and end (for parsing)"""
    rep = ""
    p = 6
    while p < len(s):
        if s[p] == '1':
            rep += s[p + 1:p + 5]
            p += 5
        elif s[p] == '0':
            rep += s[p + 1:p + 5]
            return bi(rep), p + 5


def part2(lines):
    bins = hex_to_bins(lines[0])
    return sum_vers(bins)[1]


def evaluate(type, sub_vals):
    # Non-idiomatic Python, but was too cute to resist
    ops = [
        sum,
        product,
        min,
        max,
        None,
        lambda v: 1 if v[0] > v[1] else 0,
        lambda v: 1 if v[0] < v[1] else 0,
        lambda v: 1 if v[0] == v[1] else 0
    ]
    return ops[type](sub_vals)


if __name__ == '__main__':
    main()
