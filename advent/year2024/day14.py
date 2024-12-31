from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines, tall=7, wide=11, seconds=100))
    print("Part 1:")
    print(part1(lines, tall=103, wide=101, seconds=100))
    # print("Part 2 (test):")
    # print(part2(test_lines))
    print("Part 2:")
    print(part2(lines, tall=103, wide=101))



def part1(lines, tall, wide, seconds):
    parts = [elf.septoi(line) for line in lines]
    results = [0, 0, 0, 0, 0]
    for part in parts:
        start_pos = part[1:3]
        velocity = part[-2:]
        final_pos = final(start_pos, velocity, tall, wide, seconds)
        q = quad(final_pos, tall, wide)
        results[q] += 1
    return elf.product(results[1:])


def final(start_pos, velocity, tall, wide, seconds):
    fx = (start_pos[0] + (velocity[0] * seconds)) % wide
    fy = (start_pos[1] + (velocity[1] * seconds)) % tall
    return fx, fy

def quad(pos, tall, wide):
    """Return which quadrant it's in, or 0 if it's in the middle"""
    x,y = pos
    half_tall = (tall // 2)
    half_wide = (wide // 2)
    if y == half_tall or x == half_wide:
        return 0
    elif y < half_tall:
        if x < half_wide:
            return 1
        else:
            return 2
    else:
        if x < half_wide:
            return 3
        else:
            return 4


def part2(lines, tall, wide):
    parts = [elf.septoi(line) for line in lines]
    robots = []
    for part in parts:
        start_pos = part[1:3]
        velocity = part[-2:]
        robots.append((start_pos, velocity))
    n = 0
    while True:
        results = [0, 0, 0, 0, 0]
        # final_positions = [] # only need this if you want to print it
        for robot in robots:
            start_pos, velocity = robot
            final_pos = final(start_pos, velocity, tall, wide, n)
            # final_positions.append(final_pos)
            q = quad(final_pos, tall, wide)
            results[q] += 1
        if max(results[1:]) > sum(results[1:]) // 2:
            # for r in range(tall):
            #     line = ""
            #     for c in range(wide):
            #         if (r,c) in final_positions:
            #             line += '*'
            #         else:
            #             line += ' '
            #     print(line)
            return n
        n += 1

if __name__ == '__main__':
    main()

# 237364140 too high