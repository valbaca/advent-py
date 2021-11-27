from advent import elf

"""
I really should've taken a disciplined token->parse->eval approach.
I probably would've if there were more than three ops (add, mult, parens)
Spent more time on part 2 than I should've b/c of this.
Also lucky that each number is a single digit.
"""


def apply_op(val, op, v):
    if val is None and op is None:
        return v
    elif op == '+':
        return val + v
    elif op == '*':
        return val * v
    else:
        raise RuntimeError(f"invalid apply: {val} {op} {v}")


def eval_line(line, paren_depth=0):
    val = None
    op = None
    i = 0
    while i < len(line):
        c = line[i]
        v = None
        i += 1
        if c == ' ':
            continue
        elif c == '+' or c == '*':
            op = c
        elif c == '(':
            v, sub_i = eval_line(line[i:], paren_depth + 1)
            val = apply_op(val, op, v)
            i += sub_i
        elif c == ')':
            if paren_depth > 0:
                return val, i
            else:
                raise RuntimeError("unmatched paren")
        else:
            v = int(c)
            val = apply_op(val, op, v)
    return val, i


def part1(lines):
    sums = [eval_line(line)[0] for line in lines]
    # print(sums)
    return sum(sums)


def find_close_paren_pos(s):
    open = 1
    for i, c in enumerate(s):
        if c == ')':
            open -= 1
        elif c == '(':
            open += 1
        if open == 0:
            return i
    return None


def eval_line2(line, paren_depth=0):
    val = None
    op = None
    i = 0
    while i < len(line):
        c = line[i]
        i += 1
        if c == ' ':
            continue
        elif c == '+':
            op = c
        elif c == '*':
            v, sub_i = eval_line2(line[i:], paren_depth)
            val = apply_op(val, c, v)
            i += sub_i
            op = None
        elif c == '(':
            end = i + find_close_paren_pos(line[i:])
            v, sub_i = eval_line2(line[i:end], paren_depth + 1)
            val = apply_op(val, op, v)
            i += sub_i + 1
        # elif c == ')':
        #     if paren_depth > 0:
        #         return val, i
        #     else:
        #         raise RuntimeError("unmatched paren")
        else:
            val = apply_op(val, op, int(c))
    return val, i


def part2(lines):
    sums = [eval_line2(line)[0] for line in lines]
    # print(sums)
    return sum(sums)


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
