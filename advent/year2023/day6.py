from collections import Counter, defaultdict

from advent import elf

# TIL: Good ol' binary search still does the trick

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
    times = elf.septoi(lines[0])[1:]   # Times
    records = elf.septoi(lines[1])[1:] # Distances
    out = 1
    for total_time, record in zip(times, records):
        bests = defaultdict(int) # dist: n
        for hold in range(1, total_time-1):
            dist = (total_time-hold) * hold
            bests[dist] += 1
        out *= sum(v for k, v in bests.items() if k > record)
    return out


def part2(lines):
    times = elf.septoi(lines[0])[1:]  # Times
    actual_time = int("".join([str(t) for t in times]))
    records = elf.septoi(lines[1])[1:]  # Distances
    actual_record = int("".join([str(r) for r in records]))
    def beats(n):
        return ((actual_time-n) * n) > actual_record

    start_mid = actual_time // 2

    left_out = 0
    left_ok = start_mid

    while left_ok - left_out > 1:
        left = ((left_ok - left_out) // 2 ) + left_out
        if beats(left):
            left_ok = left
        else:
            left_out = left

    right_out = actual_time
    right_ok = start_mid
    while right_out - right_ok > 1:
        right = ((right_out - right_ok) // 2 ) + right_ok
        if beats(right):
            right_ok = right
        else:
            right_out = right
    return right_ok - left_ok + 1



if __name__ == '__main__':
    main()
