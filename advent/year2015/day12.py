import json

from advent.elf import read_lines, septoi


def part1(input):
    splits = septoi(input[0])
    return sum((s if isinstance(s, int) else 0) for s in splits)


def count(obj):
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum((count(v) for v in obj))
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v == "red":
                return 0
        return sum((count(v) for v in obj.values()))
    else:
        return 0


def part2(input):
    js = json.loads(input[0])
    return count(js)


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
