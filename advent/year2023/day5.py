import math

from more_itertools import batched

from advent import elf

# TIL: working with ranges is tedious to code, yet they come up in a few Advent problems

# General case is "Range searching"
# General solns: k-d trees, range trees

# Maybe I should create a mini-range library? Or look into Segment Tree implementations?
# overlap(ra, rb) => [left_overlap, full_overlap, right_overlap]

# For these N, seems like just a sorted list of ranges works best to query against.


def main():
    test_txt = elf.lines_blank_grouped("day5-test.txt")
    print("Part 1 (test):")
    print(part1(test_txt))

    day_txt = elf.lines_blank_grouped("day5.txt")
    print("Part 1:")
    print(part1(day_txt))

    print("Part 2 (test):")
    print(part2(test_txt))

    print("Part 2:")
    print(part2(day_txt))


def part1(lines_grouped):
    seed_ids = elf.septoi(lines_grouped[0][0])[1:]
    mappings = [Mapping(group) for group in lines_grouped[1:]]
    locs = []
    for seed_id in seed_ids:
        curr_id = seed_id
        for mapping in mappings:
            curr_id = mapping.to_dest(curr_id)
        locs.append(curr_id)
    return min(*locs)


def part2(lines_grouped):
    seed_line_nums = elf.septoi(lines_grouped[0][0])[1:]
    seed_batches = batched(seed_line_nums, 2)
    mappings = [Mapping(group) for group in lines_grouped[1:]]
    min_loc = math.inf
    for seed_start, seed_len in seed_batches:
        ranges = [range(seed_start, seed_start + seed_len)]
        for mapping in mappings:
            new_ranges = [m for r in ranges for m in mapping.to_dest_range(r)]
            ranges = new_ranges
        min_loc = min(min_loc, *(r.start for r in ranges))
    return min_loc


class Mapping:
    def __init__(self, line_group):
        self.name = line_group[0]
        range_dsl = [
            elf.septoi(line)
            for line in line_group[1:]
        ]
        ranges = [
            (range(dst, dst + lng), range(src, src + lng))
            for (dst, src, lng) in range_dsl
        ]
        self.ranges_by_src = sorted(ranges, key=lambda r: r[1].start)

    def to_dest(self, n):
        if n < self.ranges_by_src[0][1].start:
            return n
        for (dst_range, src_range) in self.ranges_by_src:
            if n in src_range:
                return dst_range.start + (n - src_range.start)
        return n

    def to_dest_range(self, n_range):
        """
        given a range (start, end), returns a list of ranges of the y(x)
        e.g. given start = 1, stop = 100  and src ranges are [(20, 30)] with dst [(1000, 1010)]
        we return => [(1,20), (1000, 1010), (31, 100)]
        """
        out = []
        # Ranges are basically just (start, stop) tuples for these purposes
        # start will change as we find where it fits within our src ranges
        # stop will never change
        start, stop = n_range.start, n_range.stop
        for (dst_range, src_range) in self.ranges_by_src:
            # actual_src + offset = actual_src + (dst.s - src.s) = dst.s + (actual_src - src.s)
            offset = dst_range.start - src_range.start
            if start in src_range:
                if stop - 1 in src_range:
                    # fully within! done!
                    out.append(range(start + offset, stop + offset))
                    return out
                else:
                    # end goes beyond
                    assert dst_range.stop == offset + src_range.stop
                    out.append(range(start + offset, dst_range.stop))
                    start = src_range.stop
            elif start < src_range.start:
                # left bound
                if stop - 1 in src_range:
                    # left straddle
                    out.append(range(start, src_range.start))  # n -> n mapping
                    out.append(range(src_range.start + offset, stop + offset))  # offset
                    return out
                elif stop - 1 < src_range.start:
                    # outside left
                    out.append(range(start, stop))
                    return out
                else:
                    # full straddle
                    out.append(range(start, src_range.start))  # n -> n mapping
                    out.append(dst_range)  # offset
                    start = src_range.stop  # setup for next step
        # ran out of ranges!
        out.append(range(start, stop))  # n -> n mapping
        return out


if __name__ == '__main__':
    main()
