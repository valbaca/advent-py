import math

from advent.elf import read_lines, septoi

target = 150


def part1(input):
    buckets = sorted([septoi(line)[0] for line in input])
    ans = 0
    # First approach using combinations_with_replacement(buckets, i) was wayyy too slow. 
    # Instead using bitset to sum (similar to my Go solution)
    for i in range(0, (1 << len(buckets))):
        if subset_sum(buckets, i)[0] == target:
            ans += 1
    return ans


def part2(input):
    buckets = sorted([septoi(line)[0] for line in input])
    count, min_bucket = 0, math.inf
    for i in range(0, 1 << len(buckets)):
        ssum, length = subset_sum(buckets, i)
        if ssum == target:
            if length < min_bucket:
                min_bucket = length
                count = 1
            elif length == min_bucket:
                count += 1
    return count


def subset_sum(buckets, i):
    ssum, length = 0, 0
    for bucket in buckets:
        if i % 2 == 1:
            ssum += bucket
            length += 1
        i >>= 1
    return ssum, length


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
