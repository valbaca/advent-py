from collections import defaultdict

from advent import elf


def main():
    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))

def exec(lines, reg=defaultdict(int)):
    def var(x):
        return x if isinstance(x, int) else reg[x]
    ins = [elf.septoi(line) for line in lines]
    ip = 0
    while 0 <= ip < len(ins):
        cmd = ins[ip]
        x = var(cmd[1])
        match cmd[0]:
            case 'cpy':
                reg[cmd[2]] = x if isinstance(x, int) else reg[x]
            case 'inc':
                reg[cmd[1]] += 1
            case 'dec':
                reg[cmd[1]] -= 1
            case 'jnz':
                if x != 0:
                    ip += var(cmd[2])
                    continue
        ip += 1
    return reg

def part1(lines):
    return exec(lines)['a']

def part2(lines):
    reg = defaultdict(int)
    reg['c'] = 1
    return exec(lines, reg)['a']


if __name__ == '__main__':
    main()
