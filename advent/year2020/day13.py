from advent import elf
from advent.elf import safe_atoi

"""
This question was wild.
The first part was very trivial and the second had me reaching out to StackOverflow.
Thankfully, someone had a working example for the case of two buses (or runners) and 
I just had to adapt it to work with more buses.
"""


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
    inputs = []
    for line in lines[1:]:
        inputs.append(list(map(safe_atoi, line.split(","))))
    return inputs


# Stealing from https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset

def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def solve_part2(buses):
    all_period, all_phase = 1, 0  # identity
    for phase, period in enumerate(buses):
        if period == 'x':
            continue
        all_period, all_phase = combine_phased_rotations(all_period, all_phase, period, phase)
    return all_period - all_phase


def part2(lines):
    return list(map(solve_part2, parse_part2(lines)))


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
