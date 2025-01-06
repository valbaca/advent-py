from functools import cache

from advent import elf

# Took me WAY too long to stop being stubborn and just read the assembly code and figure out that it was like a past
# year's problem of ((((x0) * 8) + x1)*8 + x2)*8 etc.

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    a, program = parse(lines)
    output,_ = go(a, program)
    return ','.join(str(n) for n in output)


def parse(lines):
    for line in lines:
        if line.startswith("Register A"):
            a = elf.only_ints(elf.septoi(line))[0]
        if line.startswith("Program"):
            program = elf.only_ints(elf.septoi(line))  # type: list[int]
    return a, tuple(program)

@cache
def go(a, program):
    regs = {
        'a': a,
        'b': 0,
        'c': 0,
    }
    ip = 0
    output = []
    def combo(operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return regs['a']
        elif operand == 5:
            return regs['b']
        elif operand == 6:
            return regs['c']
        else:
            raise Exception()

    while 0 <= ip < len(program):
        opcode, operand = program[ip], program[ip+1]
        jumped = False
        if opcode == 0:
            num, den = regs['a'], 2 ** combo(operand)
            regs['a'] = num // den
        elif opcode == 1:
            regs['b'] ^= operand
        elif opcode == 2:
            comb = combo(operand)
            regs['b'] = comb % 8
        elif opcode == 3:
            if regs['a'] != 0:
                ip = operand
                jumped = True
        elif opcode == 4:
            regs['b'] = regs['b'] ^ regs['c']
        elif opcode == 5:
            comb = combo(operand)
            output.append(comb % 8)
        elif opcode == 6:
            num, den = regs['a'], 2 ** combo(operand)
            regs['b'] = num // den
        elif opcode == 7:
            num, den = regs['a'], 2 ** combo(operand)
            regs['c'] = num // den
        else:
            raise Exception()
        if not jumped:
            ip += 2
    return output, (regs['a'], regs['b'], regs['c'])




"""
2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0

bst A; B = A % 8
bxl 2; B = B ^ 2
cdv B; C = A / (2**B)
bxc _; B = B ^ C
adv 3; A = A / (2**3)
bxl 7; B = B ^ 7
out B; **output B**
jnz 0; if A != 0: jump to 0
"""

def prog(a):
    b0 = a % 8
    b1 = b0 ^ 2
    c = a // (2**b1)
    b2 = b1 ^ c
    return a // 8, (b2 ^ 7) % 8

def part2(lines):
    _, program = parse(lines)
    ans = 0
    for p in reversed(program):
        for a0 in range(8):
            out_a, b = prog(ans*8 + a0)
            if out_a == ans and b == p:
                ans = ans*8 + a0
                break
    return ans

# part 2: 190384615275535, [5, 3, 2, 2, 3, 5, 3, 7, 2, 7, 2, 3, 6, 0, 1, 7]


if __name__ == '__main__':
    main()

"""
Leaving this code as a testament to all the b.s. I tried...



def part2_brute(lines):
    orig_regs, program = parse(lines)
    # n = 202478532771599
    n = 202400000000000
    while True:
        regs = orig_regs.copy()
        regs['a'] = n
        output = go(regs, program, tgt=program)
        # print(output)
        if output == program:
            return n
        # else:
        #     print(f"{n=} => {output=}")
        n += 1


def part2_meh(lines):
    orig_regs, program = parse(lines)
    program = tuple(program)

    q = [()]
    for t in program:
        next_q = set()
        # print(f"{q=}")
        for prev_as in q:
            for n in range(N):
                output, regs = go(n, program)
                if output[0] == t:
                    next_prev_as = list(prev_as)
                    next_prev_as.append(n)
                    # b is immediately overwritten, so don't need to "save" it
                    next_q.add(tuple(next_prev_as))
                    # xa = 0
                    # for n in reversed(next_prev_as):
                    #     xa *= 8
                    #     xa += n
                    # verify, _ = go(xa, program)
                    # if verify == program[:len(verify)]:
                    #     next_q.add(tuple(next_prev_as))

        print(f"{t=}")
        # q = sorted(set(next_q))
        q = next_q
    # print(f"{q=}")
    ans = set(q)
    # for a in ans:
    #     print(a)

    for a in sorted(ans):
        print(a)
        xa = 0
        for n in reversed(a):
            xa *= 8
            xa += n
        # regs = orig_regs.copy()
        # regs['a'] = xa
        verify_output, _ = go(xa, program)
        # print(f"Trying {xa=}, gives {verify_output=}")
        if tuple(verify_output) == program:
            return xa
        else:
            print(f"We wanted {program=} but got {verify_output=}")
    # return ans

    # ans = 0
    # using = arr[:3]
    # print(f"{using=}")
    # for n in reversed(using):
    #     ans *= 8
    #     ans += n
    # regs = orig_regs.copy()
    # regs['a'] = ans
    # verify_output = go(regs, program)
    # print(f"{program}")
    # if verify_output == program:
    #     return ans
    # else:
    #     return f"{ans=} was not the answer; {verify_output=}"


def messing(program):
    print(go({'a': 117440, 'b': 0, 'c': 0}, program))
    d = 117440
    while True:
        d, m = divmod(d, 8)
        print(d, m)
        if d == 0:
            break



def part2_xxx(lines):
    # 5 [3,7] 2....
    # gotta automate this!
    for a in range(8**2):
        out_a, b = prog(8*8*5 + 8*7 + a)
        if out_a == (8*5 + 7) and b == 5:
            print(a)
"""