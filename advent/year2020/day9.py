from advent.elf import read_lines, safe_atoi, even, bisect_index

"""
bisect and prefix sums are key
"""


def main():
    lines = read_lines(__file__, safe_atoi)
    target = part1(lines)
    print(target)
    print(part2(lines, target))


PLEN = 25


def in_preamble(n, pre):
    # handle the case where n/2 is present twice
    if even(n) and pre.count(n // 2) >= 2:
        return True
    sorted_pre = sorted(pre)
    for i, e in enumerate(sorted_pre):
        bi = bisect_index(sorted_pre[i + 1:], n - e)
        if bi is not None:
            return True
    return False


def part1(lines):
    for end in range(PLEN, len(lines)):
        if not in_preamble(lines[end], lines[end - PLEN:end]):
            return lines[end]
    return None


def part2(lines, target):
    pfs = lines.copy()  # prefix sums
    for i in range(1, len(pfs)):
        pfs[i] += pfs[i - 1]
    for i, e in enumerate(pfs):
        bi = bisect_index(pfs[i + 1:], e + target)
        if bi is not None:
            sub_seq = lines[i:i + 1 + bi]
            return max(sub_seq) + min(sub_seq)
    return None


if __name__ == '__main__':
    main()
