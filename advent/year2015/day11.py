from functools import cache
from advent.elf import read_lines


def inc_char(c):
    return chr(ord(c) + 1)


def inc(s):
    out = []
    carry = True
    for c in s[::-1]:
        if carry:
            if c == "z":
                c = "a"
                carry = True
            else:
                c = inc_char(c)
                carry = False
            if c in "iol":
                c = inc_char(c)
        out.append(c)
    if carry:
        out.append("a")
    return "".join(out[::-1])


def has_straight(s):
    for i in range(len(s) - 2):
        if ord(s[i]) == ord(s[i + 1]) - 1 == ord(s[i + 2]) - 2:
            return True
    return False


def has_double_pair(s):
    i = 1
    pairs = set()
    while i < len(s):
        p, c = s[i - 1], s[i]
        if p == c:
            pair = f"{p}{c}"
            if pair not in pairs and len(pairs) > 0:
                return True
            pairs.add(pair)
            i += 1
        i += 1
    return False


def meets_reqs(s):
    return has_straight(s) and has_double_pair(s)

@cache
def next_password(s):
    s = inc(s)
    while not meets_reqs(s):
        s = inc(s)
    return s

def part1(input):
    return next_password(input[0])


def part2(input):
    return next_password(next_password(input[0]))


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
