from collections import Counter
from advent.elf import read_lines

def part1(input):
    return sum((is_nice(s) for s in input))

def is_nice(s):
    return has_three_vowels(s) and has_double(s) and not has_forbidden(s)

def has_three_vowels(s):
    counts = Counter(s)
    return sum((counts[vowel]) for vowel in "aeiou") >= 3

def has_double(s):
    prev = s[0]
    for ch in s[1::]:
        if prev == ch:
            return True
        prev = ch
    return False

def has_forbidden(s: str):
    return any((forb in s) for forb in ["ab", "cd", "pq", "xy"])

def part2(input):
    return sum((has_repeat(s) and has_double(s)) for s in input)

def has_repeat(s):
    for i in range(len(s)-2):
        a, c = s[i], s[i+2]
        if a == c:
            return True
    return False

def has_double(s):
    seen = set()
    overlap = s[0:2] # the previous pair, held to prevent checking the overlapping string
    for i in range(1, len(s)-1):
        curr = s[i:i+2]
        if curr in seen:
            return True
        seen.add(overlap)
        overlap = curr
    return False

if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
