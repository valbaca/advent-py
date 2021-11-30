from advent.elf import read_lines


def main():
    inp = read_lines(__file__)
    seats = list(map(score, inp))
    print(max(seats))

    part2(seats)


def binary_str(s, zero):
    return int(str.join("", map(lambda c: '0' if c == zero else '1', list(s))), 2)


def str_to_row(s):
    return binary_str(s, 'F')


def str_to_seat(s):
    return binary_str(s, 'L')


def score(s):
    return str_to_row(s[:7]) * 8 + str_to_seat(s[7:])


def part2(seats):
    seats = sorted(seats)
    # this could be done more optimally in only lg(n) checks, but this simply works well enough
    for i in range(min(seats), max(seats)):
        if i not in seats:
            print(i)


if __name__ == '__main__':
    main()
