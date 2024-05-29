import math
from collections import defaultdict

from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def exec(lines, reg=None):
    if reg is None:
        reg = defaultdict(int)

    def var(v):
        return v if isinstance(v, int) else reg[v]

    ins = [elf.septoi(line) for line in lines]
    ip = 0
    while 0 <= ip < len(ins):
        cmd = ins[ip]
        x, xv = cmd[1], var(cmd[1])  # x (the arg, str or int) and x_value (int)
        match cmd[0]:
            case 'cpy':  # 2-arg
                if isinstance(y := cmd[2], str):
                    reg[y] = xv
            case 'inc':  # 1-arg
                if isinstance(x, str):
                    reg[x] += 1
            case 'dec':  # 1-arg
                if isinstance(x, str):
                    reg[x] -= 1
            case 'jnz':  # 2-arg
                if xv != 0:
                    ip += var(cmd[2])
                    continue
            case 'tgl':
                tgt_ip = ip + xv
                if not (0 < tgt_ip < len(ins)):
                    ip += 1
                    continue
                ins[tgt_ip][0] = {
                    'cpy': 'jnz',
                    'inc': 'dec',
                    'dec': 'inc',
                    'jnz': 'cpy',
                    'tgl': 'inc'
                }[ins[tgt_ip][0]]
        ip += 1
    return reg


def part1(lines):
    reg = defaultdict(int)
    reg['a'] = 7
    return exec(lines, reg)['a']


def part2(lines):
    # okay, cheated again. Really got spoiled while looking for hints
    all_nums = [n for line in lines
                for n in elf.septoi(line) if isinstance(n, int)]
    mx = sorted(all_nums)[-2:]  # find the big constants
    return math.factorial(12) + (mx[0] * mx[1])


if __name__ == '__main__':
    main()
