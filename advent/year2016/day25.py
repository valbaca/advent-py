import itertools
from collections import defaultdict

from advent import elf


def main():
    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


# Using a limit isn't technically correct, but it works
def exec(lines, init_a=0):
    reg = defaultdict(int)
    reg['a'] = init_a

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
                    'tgl': 'inc',
                    'out': 'inc'
                }[ins[tgt_ip][0]]
            case 'out':
                yield xv
        ip += 1


def part1(lines):
    wants = list(itertools.islice(itertools.cycle([0, 1]), 0, 1000))
    for init_a in range(40_000_000_000):
        sig_gen = exec(lines, init_a=init_a)
        if all(actual == want for actual, want in zip(sig_gen, wants)):
            return init_a


def part2(lines):
    return "Merry Christmas! 🎄🐍⭐️"


if __name__ == '__main__':
    main()
