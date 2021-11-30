from advent import elf
from advent.elf import safe_atoi

"""
This question was wild.
The first part was very trivial and the second had me reaching out to StackOverflow.
Thankfully, someone had a working example for the case of two buses (or runners) and 
I just had to adapt it to work with more buses.
"""


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


def lines_to_input(lines):
    return int(lines[0]), list(map(safe_atoi, filter(lambda x: x != 'x', lines[1].split(","))))


def next_depart(earliest, schedule):
    return schedule + schedule * (earliest // schedule)


def part1(lines):
    earliest, schedules = lines_to_input(lines)
    ids_times = list(map(lambda x: (next_depart(earliest, x), x), schedules))
    earliest_bus_time, bus_id = min(ids_times)

    return bus_id * (earliest_bus_time - earliest)


def parse_part2(lines):
    return list(map(safe_atoi, lines[1].split(",")))


def solve_part2(buses):
    all_period, all_phase = 1, 0  # identity
    for phase, period in enumerate(buses):
        if period == 'x':
            continue
        all_period, all_phase = elf.combine_phased_rotations(all_period, all_phase, period, phase)
    return all_period - all_phase


def part2(lines):
    return solve_part2(parse_part2(lines))


if __name__ == '__main__':
    main()
