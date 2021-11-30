import re

from advent import elf

"""
Another classic advent where part 1 is trivial and part 2 takes way more advanced tactics.
Honestly, my part 2 is a brute-force pile of code.
My approach is similar to a human brute-force solution for Sudoku.
Keep a list of list of ticket indexes where a field *could* be and remove them based on the tickets.
Eventually you end up with one (or more) fields that only correspond to a single index.
You remove that index from all the other fields' possible indexes.
Do that enough and (hopefully) you should have only one for each.

I do start to miss a few of clojure's built in sequence functions, maybe I should write my own?
- filter/map/reduce: proper ones that can be chained
I guess that's the major power of FP is there's less necessary distinction between lazy and eager.
FP can be as lazy as it can be

List comprehensions are close though.

- group-by and partition-by
Ironically something that was challenging in Clojure (creating a "collected" kind of list) is also not super
clean in python.

- flatten
Need to just write my own
"""


def main():
    line_groups = elf.lines_blank_grouped(elf.in_file(__file__))
    print(part1(line_groups))
    print(part2(line_groups))


def parse_ranges(line):
    strs = [elf.safe_atoi(s) for s in re.split(r"[\D]", line)]
    strs = [s for s in strs if isinstance(s, int)]
    ranges = []
    for i in range(0, len(strs), 2):
        ranges.append([strs[i], strs[i + 1]])
    return ranges


def parse_ticket(line):
    return [int(s) for s in line.split(",")]


def parse(line_groups):
    range_lines, your_ticket_lines, nearby_tickets = line_groups
    ranges = [parse_ranges(line) for line in range_lines]
    your_ticket = parse_ticket(your_ticket_lines[1])
    tickets = [parse_ticket(line) for line in nearby_tickets[1:]]
    return ranges, your_ticket, tickets


def is_valid_for_any(ranges, n):
    for range_set in ranges:
        for r in range_set:
            mn, mx = r
            if mn <= n <= mx:
                return True
    return False


def part1(line_groups):
    ranges, _, tickets = parse(line_groups)
    invalid_vals = []
    for ticket in tickets:
        for val in ticket:
            if not is_valid_for_any(ranges, val):
                invalid_vals.append(val)
    return sum(invalid_vals)


def is_valid_ticket(ticket, ranges):
    for val in ticket:
        if not is_valid_for_any(ranges, val):
            return False
    return True


def is_reduced(lst):
    for x in lst:
        if len(x) == 0:
            raise RuntimeError("uh oh")
        if len(x) != 1:
            return False
    return True


def reduce_possible_fields(possible_field_idx):
    reduced = possible_field_idx[:]
    while not is_reduced(reduced):
        to_remove = [lst[0] for lst in reduced if len(lst) == 1]
        for lst in reduced:
            if len(lst) == 1:
                continue
            for rm in to_remove:
                if rm in lst:
                    lst.remove(rm)
    return reduced


def part2(line_groups):
    ranges, your_ticket, tickets = parse(line_groups)
    valid_tickets = [t for t in tickets if is_valid_ticket(t, ranges)]
    possible_fields = [list(range(len(ranges))) for _ in range(len(ranges))]
    for field_num, range_set in enumerate(ranges):
        for ticket in valid_tickets:
            for val_idx, val in enumerate(ticket):
                if val_idx in possible_fields[field_num] and not is_valid_for_any([range_set], val):
                    possible_fields[field_num].remove(val_idx)
    reduced_fields = reduce_possible_fields(possible_fields)
    fields = [idx for fields in reduced_fields for idx in fields]
    # first six fields start with "departure"
    return elf.product([your_ticket[i] for i in fields[:6]])


if __name__ == '__main__':
    main()
