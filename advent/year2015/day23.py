from advent.elf import even, read_lines, septoi


def part1(input):
    return exec(input)


def exec(input, a_start=0):
    input = [septoi(line, r"[, ]") for line in input]
    regs = {"a": a_start, "b": 0}
    ip = 0
    while 0 <= ip < len(input):
        inst, prev_ip = input[ip], ip
        op = inst[0]
        if op == 'hlf':
            regs[inst[1]] /= 2
        elif op == 'tpl':
            regs[inst[1]] *= 3
        elif op == 'inc':
            regs[inst[1]] += 1
        elif op == 'jmp':
            ip += inst[1]
        elif op == 'jie':
            if even(regs[inst[1]]):
                ip += inst[2]
        elif op == "jio":
            if 1 == regs[inst[1]]:
                ip += inst[2]
        if ip == prev_ip:
            ip += 1
    return regs["b"]


def part2(input):
    return exec(input, 1)


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
