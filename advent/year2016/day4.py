import heapq
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappush


def main():
    total = 0
    with open('day4.txt') as file:
        for line in file.readlines():
            ln = line.strip()
            if is_real(ln):
                sector_id = get_sector_id(ln)
                total += sector_id
                # print them all and ctrl-f for "pole"
                print(rotate(ln), sector_id)
    print(total)


def rotate(s: str):
    sector_id = get_sector_id(s)
    msg = s[:s.rindex('-')]
    rot_msg = [rotate_char(c, sector_id) for c in msg]
    return ''.join(rot_msg)


def rotate_char(s, id):
    if s == '-':
        return ' '
    i = ord(s) - 97 + id
    return chr((i % 26) + 97)


def get_sector_id(s) -> int:
    end = s.find('[')
    if end == -1:
        end = len(s)
    start = s[:end].rindex('-')
    return int(s[start + 1:end])


def is_real(s):
    checksum = get_checksum(s)
    actual_sum = generate_sum(s)
    return checksum == actual_sum


def get_checksum(s: str):
    return s[s.index('[') + 1:-1]


def generate_sum(s: str):
    checksum_idx = s.index('[')
    name = s[:checksum_idx]
    counts = defaultdict(int)
    for c in name:
        if c.isalpha():
            counts[c] += 1
    pq = []
    for k, v in counts.items():
        heappush(pq, CharCount(v, -ord(k), k))
    checksum_len = min(len(s) - checksum_idx - 2, len(pq))
    largest_counts = heapq.nlargest(checksum_len, pq)
    chars = [x.char for x in largest_counts]
    return ''.join(chars)


@dataclass(order=True)
class CharCount:
    count: int
    # storing the char as a negative number,
    # rev alpha keeps alphabetic order
    # w/ heapq.nlargest
    rev_alpha: int
    char: str


if __name__ == '__main__':
    main()
