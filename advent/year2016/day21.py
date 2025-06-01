import itertools
from advent import elf
# TIL: you cannot (easily?) reverse the rotate based on position
# but computers are fast and this is babys-first-password cracking

# TIL: neat rotate trick. Rotates left if n is positive, or right if n is negative
# n  = n % len(s)
# s = s[n:] + s[:n]

def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def part1(lines):
    s = "abcdefgh"
    for line in lines:
        # print(f"{s=} {line=}")
        s = perform(s, line)
        # print(s)
    return s

def perform(in_s: str, line):
    s = list(in_s)
    seps = elf.septoi(line)
    # print(f"{line=} {seps=}")
    if line.startswith("swap position"):
        a, b = seps[2], seps[-1]
        s[a], s[b] = s[b], s[a]
    elif line.startswith("swap letter"):
        a, b = seps[2], seps[-1]
        pa = in_s.find(a)
        pb = in_s.find(b)
        s[pa], s[pb] = s[pb], s[pa]
    elif line.startswith("reverse positions"):
        a, b = seps[2], seps[-1]
        s = s[:a] + s[a:b+1][::-1] + s[b+1:]
    elif line.startswith("rotate left"):
        n = seps[2]
        n  = n % len(s)
        s = s[n:] + s[:n]
    elif line.startswith("rotate right"):
        n = seps[2]
        n  = (-n) % len(s)
        s = s[n:] + s[:n]
    elif line.startswith("move position"):
        a, b = seps[2], seps[-1]
        c = s[a] # char
        ts = s[:a] + s[a+1:] # temp str
        s = ts[:b] + [c] + ts[b:] # re-insert
    elif line.startswith("rotate based on position"):
        c = seps[-1]
        p = in_s.find(c)
        rots = 1 + p + (1 if p >= 4 else 0)
        # rotate right
        n = (-rots) % len(s)
        s = s[n:] + s[:n]
    else:
        raise Exception(f"unknown {line=}")
    if len(s) != len(in_s):
        raise Exception(f"broken! {in_s=} {"".join(s)} {line=}")
    return "".join(s)

def part2(lines):
    for start in map("".join, itertools.permutations("abcdefgh")):
        s = start
        for line in lines:
            s = perform(s, line)
        if s == "fbgdceah":
            return start


if __name__ == '__main__':
    main()
