from advent import elf

"""
This is the kind of advent that I like.
The first part is straightforward enough, but to really solve the second part,
you're much better off with a custom object (obj) type to turn O(n) operations into O(1) ones
"""


def rindex(a, e):
    if e not in a:
        return None
    return len(a) - a[::-1].index(e) - 1


def next_num(a):
    last = a[-1]
    but_last = a[:-1]
    if last not in but_last:
        return 0
    rev = but_last[::-1]
    rev_idx = rev.index(last)
    return rev_idx + 1


def part1(lines):
    ints = list(map(int, lines[0].split(",")))
    while len(ints) < 2020:
        ints.append(next_num(ints))
    return ints[-1]


def create_counting_obj(first):
    return {'last': first, 'len': 1, 'idx': {first: 0}}


def append_num(obj, n):
    obj['idx'][obj['last']] = obj['len'] - 1
    obj['last'] = n
    obj['len'] += 1


def next_counting_num(obj):
    last = obj['last']
    if last not in obj['idx']:
        return 0
    idx = obj['idx'][last]
    return obj['len'] - idx - 1


def part2(lines):
    ints = list(map(int, lines[0].split(",")))
    obj = create_counting_obj(ints[0])
    for i in ints[1:]:
        append_num(obj, i)

    while obj['len'] < 30000000:
        append_num(obj, next_counting_num(obj))
    return obj['last']


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
