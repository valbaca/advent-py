import re

from advent import elf


def parse_ranges(line):
    strs = map(elf.safe_atoi, re.split(r"[\D]", line))
    strs = list(filter(lambda s: isinstance(s, int), strs))
    ranges = []
    for i in range(0, len(strs), 2):
        ranges.append([strs[i], strs[i + 1]])
    return ranges


def parse_ticket(line):
    return [int(s) for s in line.split(",")]


def parse_p1(line_groups):
    range_lines, your_ticket_lines, nearby_tickets = line_groups
    ranges = [parse_ranges(line) for line in range_lines]
    tickets = [parse_ticket(line) for line in nearby_tickets[1:]]
    return ranges, tickets


def is_valid_for_any(ranges, n):
    for range_set in ranges:
        for r in range_set:
            mn, mx = r
            if mn <= n <= mx:
                return True
    return False


def part1(line_groups):
    ranges, tickets = parse_p1(line_groups)
    invalid_vals = []
    for ticket in tickets:
        for val in ticket:
            if not is_valid_for_any(ranges, val):
                invalid_vals.append(val)
    # print(invalid_vals)
    return sum(invalid_vals)


def part2(lines):
    pass
    # code here


def main():
    line_groups = elf.lines_blank_grouped(elf.in_file(__file__))
    print(part1(line_groups))
    print(part2(line_groups))


if __name__ == '__main__':
    main()
