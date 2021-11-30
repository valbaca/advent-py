from advent.elf import read_lines, septoi


def main():
    lines = read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


def part1(lines, acc=0, ip=0, execd=None):
    if not execd:
        execd = set()
    while 0 <= ip < len(lines) and ip not in execd:
        execd.add(ip)
        op, arg = septoi(lines[ip])
        if op == "nop":
            ip += 1
        elif op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            ip += arg
        else:
            raise RuntimeError(f"{op} is not an operation")
    return acc, ip == len(lines)


def part2(lines, acc=0, ip=0, execd=None, changed=False):
    if not execd:
        execd = set()
    while 0 <= ip < len(lines) and ip not in execd:
        execd.add(ip)
        op, arg = septoi(lines[ip])
        if op == "nop":
            if not changed:
                sub_acc, sub_solved = part2(lines, acc, (ip + arg), set(execd), True)
                if sub_solved:
                    return sub_acc, sub_solved
            ip += 1
        elif op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            if not changed:
                sub_acc, sub_solved = part2(lines, acc, (ip + 1), set(execd), True)
                if sub_solved:
                    return sub_acc, sub_solved
            ip += arg
        else:
            raise RuntimeError(f"{op} is not an operation")
    return acc, ip == len(lines)


if __name__ == '__main__':
    main()
