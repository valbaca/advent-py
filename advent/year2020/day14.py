import re

from advent import elf

"""
This was not a very elegant solution, but we got there.

The 'float' bits are simplified by doing an xor flag, since xor 1 flips a bit.
"""


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


def parse_mask(line):
    line = line[7:]
    set_bits_str = ''.join(map(lambda c: '1' if c == '1' else '0', list(line)))
    set_bits = int(set_bits_str, 2)
    clear_bits_str = ''.join(map(lambda c: '0' if c == '0' else '1', list(line)))
    clear_bits = int(clear_bits_str, 2)
    return set_bits, clear_bits


def parse_mem(line):
    add, val = map(elf.safe_atoi, filter(lambda s: s != "", re.split(r"[\D]", line)))
    return add, val


def apply_mask(mask, val):
    set_bits, clear_bits = mask
    val |= set_bits
    val &= clear_bits
    return val


def part1(lines):
    mask = None
    mem = {}
    for line in lines:
        if line.startswith('mask'):
            mask = parse_mask(line)
        else:
            add, val = parse_mem(line)
            mem[add] = apply_mask(mask, val)
    return sum(mem.values())


def parse_mask_p2(line):
    set_bits, clear_bits = parse_mask(line)
    line = line[7:]
    base_mask = '0' * 36
    xor_masks = []
    for i, char in enumerate(list(line)):
        if char == 'X':
            xor_mask = elf.str_replace(base_mask, i, '1')
            xor_masks.append(int(xor_mask, 2))
    return set_bits, clear_bits, xor_masks


def generate_mems(xor_masks, add):
    addresses = [add]  # start with initial
    for xor_mask in xor_masks:
        # each xor_mask only flips a single bit
        # this has to iterate over a copy, addresses[:], to not cause issues
        for a in addresses[:]:
            addresses.append(a ^ xor_mask)
    return addresses


def update_mem_p2(mem, mask, add, val):
    set_bits, _, xor_masks = mask
    # ignore clear bits
    base_add = add | set_bits
    # mem[base_add] = val
    xor_addresses = generate_mems(xor_masks, base_add)
    for xor_add in xor_addresses:
        mem[xor_add] = val


def part2(lines):
    mask = None
    mem = {}
    for line in lines:
        if line.startswith('mask'):
            mask = parse_mask_p2(line)
        else:
            add, val = parse_mem(line)
            update_mem_p2(mem, mask, add, val)
    return sum(mem.values())


if __name__ == '__main__':
    main()
