import collections

from advent import elf

"""TIL: careful with set("string") as it will expand out the string and put the chars into the set"""

def main():
    test_lines = elf.read_lines(__file__, test=True)
    test_lines2 = elf.read_lines("day12-test2.txt", test=True)
    test_lines3 = elf.read_lines("day12-test3.txt", test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1 (test2):")
    print(part1(test_lines2))
    print("Part 1 (test3):")
    print(part1(test_lines3))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2 (test2):")
    print(part2(test_lines2))
    print("Part 2 (test3):")
    print(part2(test_lines3))
    print("Part 2:")
    print(part2(lines))


def parse(lines):
    graph = collections.defaultdict(list)
    for line in lines:
        [frm, to] = line.split("-")[:2]
        graph[frm].append(to)
        graph[to].append(frm)
    return graph

def is_small(id):
    return str.islower(id)

def gen_opts(graph, path, seen):
    last = path[-1]
    opts = []
    for nxt in graph[last]:
        if not is_small(nxt) or (is_small(nxt) and nxt not in seen):
            nxt_seen = seen.copy()
            nxt_seen.add(nxt)
            opts.append(([*path, nxt], nxt_seen))
    return opts

def part1(lines):
    graph = parse(lines)
    ans = set()
    start_set = set()
    start_set.add("start")
    opts = [(["start"], start_set)]
    while len(opts) > 0:
        path, seen = opts.pop()
        if path[-1] == "end":
            ans.add(tuple(path))
        else:
            opts.extend(gen_opts(graph, path, seen))
    return len(ans)


def gen_opts2(graph, path, seen, twice):
    last = path[-1]
    opts = []
    for nxt in graph[last]:
        if nxt == "start":
            continue
        if twice:
            # twice visit has been spent, same old logic, but keeping track of 'twice'
            if not is_small(nxt) or (is_small(nxt) and nxt not in seen):
                nxt_seen = seen.copy()
                nxt_seen.add(nxt)
                opts.append(([*path, nxt], nxt_seen, twice))
        else:
            # can use a single twice visit
            nxt_seen = seen.copy()
            nxt_seen.add(nxt)
            nxt_twice = is_small(nxt) and nxt in seen # is this a "twice" visit?
            opts.append(([*path, nxt], nxt_seen, nxt_twice))
    return opts

def part2(lines):
    graph = parse(lines)
    ans = set()
    start_set = set()
    start_set.add("start")
    opts = [(["start"], start_set, False)]
    while len(opts) > 0:
        path, seen, twice = opts.pop()
        if path[-1] == "end":
            ans.add(tuple(path))
        else:
            opts.extend(gen_opts2(graph, path, seen, twice))
    return len(ans)


if __name__ == '__main__':
    main()
