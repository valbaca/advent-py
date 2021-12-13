from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    fault_lines = [parse(line) for line in lines]
    fault_lines = [fl for fl in fault_lines if horz_or_vert(fl)]
    return count_overlaps(fault_lines)


def count_overlaps(fault_lines):
    overlap_points = {}
    for fault_idx, fault in enumerate(fault_lines):
        if fault == fault_lines[-1]:
            continue
        for x, y in points(fault):
            for other_line in fault_lines[fault_idx + 1:]:
                if overlaps(x, y, other_line):
                    if x not in overlap_points:
                        overlap_points[x] = [y]
                    elif y not in overlap_points[x]:
                        overlap_points[x].append(y)
    total = 0
    for ys in overlap_points.values():
        total += len(ys)
    return total


def order_range(a, b):
    return range(min(a, b), max(a, b) + 1)


def points(fault):
    x1, y1, x2, y2 = fault
    if x1 == x2 or y1 == y2:
        if x1 == x2:
            return [(x1, y) for y in order_range(y1, y2)]
        else:
            return [(x, y1) for x in order_range(x1, x2)]
    # else, 45deg sloped line...
    xs = order_range(x1, x2)
    if xs[0] == x2:
        xs = list(reversed(xs))
    ys = order_range(y1, y2)
    if ys[0] == y2:
        ys = list(reversed(ys))
    return zip(xs, ys)


def parse(line):
    return [n for n in elf.septoi(line) if n != '-']


def horz_or_vert(fault):
    x1, y1, x2, y2 = fault
    return x1 == x2 or y1 == y2


def find_bounds(fault_lines):
    min_x, max_x, min_y, max_y = fault_lines[0]
    for fault in fault_lines:
        x1, y1, x2, y2 = fault
        min_x = min(min_x, x1, x2)
        max_x = max(max_x, x1, x2)
        min_y = min(min_y, y1, y2)
        max_y = max(max_y, y1, y2)
    return min_x, max_x, min_y, max_y


def overlaps(x, y, fault):
    x1, y1, x2, y2 = fault
    if x1 == x2 or y1 == y2:
        return elf.between(x, x1, x2) and elf.between(y, y1, y2)
    return (x, y) in points(fault)


def part2(lines):
    fault_lines = [parse(line) for line in lines]
    return count_overlaps(fault_lines)


if __name__ == '__main__':
    main()
