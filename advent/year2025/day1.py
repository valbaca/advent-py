import elf


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
    dial = 50
    count = 0
    for line in lines:
        dir, val = line[0], int(line[1:])
        dial = dial + val if dir == "R" else dial - val
        dial  = (dial % 100)
        if dial == 0:
            count += 1
    return count



def part2(lines):
    dial = 50
    count = 0
    for line in lines:
        prev_dial, prev_count = dial, count
        dir, val = line[0], int(line[1:])
        un_mod_dial = dial + val if dir == "R" else dial - val
        rots, dial  = divmod(un_mod_dial, 100)
        if dial == 0:
            count += 1
        if dir == "R":
            count += rots
            if dial == 0:
                count -= 1
        else:
            count += (-rots)
            if prev_dial == 0:
                count -= 1
        # if count != prev_count:
            # print(f"{line} went from {prev_dial}->{dial}, {prev_count}->{count}")
    return count

if __name__ == '__main__':
    main()
