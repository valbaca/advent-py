from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def marker(s):
    if s[0] != '(':
        raise Exception(f"Expected '(' but got {s}")

    num_chars, repeat, seen_x = [], [], False
    i = 0
    while i < len(s) - 1:
        i += 1
        if s[i] == 'x':
            seen_x = True
        elif s[i] == ')':
            return int(''.join(num_chars)), int(''.join(repeat)), i + 1  # num_chars, repeat, n
        else:
            if seen_x:
                repeat.append(s[i])
            else:
                num_chars.append(s[i])


def decompress(s, v2=False):
    if '(' not in s:
        return len(s)
    total = 0
    i = 0
    while i < len(s):
        if s[i] == '(':
            num_chars, repeat, offset = marker(s[i:])
            sub_s = s[i + offset:i + offset + num_chars]
            len_sub_s = decompress(sub_s, v2) if v2 else len(sub_s)
            total += repeat * len_sub_s
            i += offset + num_chars
        else:
            total += 1
            i += 1
    return total


def part1(lines):
    return sum(decompress(line) for line in lines)


def part2(lines):
    return sum(decompress(line, v2=True) for line in lines)


if __name__ == '__main__':
    main()
