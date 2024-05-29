import hashlib

from advent.elf import read_lines


def part1(input):
    return hack(input[0], "00000")


def hack(key, prefix):
    ans = 0
    while True:
        hash = hashlib.md5(f"{key}{ans}".encode()).hexdigest()
        if hash.startswith(prefix):
            return ans
        ans += 1


def part2(input):
    return hack(input[0], "000000")


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
