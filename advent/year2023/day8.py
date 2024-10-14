import math
from itertools import cycle

from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1 (test 2):")
    print(part1(elf.read_lines("day8-test2.txt")))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2 (test 2):")
    print(part1(elf.read_lines("day8-test2.txt")))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    instr = list(lines[0])
    network = {}
    for line in lines[1:]:
        (node_id, left, right) = elf.septoi(line)
        network[node_id] = (left, right)
    cur = "AAA"
    count = 0
    while cur != "ZZZ":
        for inst in instr:
            node = network[cur]
            cur = node[0 if inst == 'L' else 1]
        count += len(instr)
    return count


def part2(lines):
    instr = list(lines[0])
    network = {}
    for line in lines[1:]:
        (node_id, left, right) = elf.septoi(line)
        network[node_id] = (left, right)
    curs = [n for n in network.keys() if n.endswith('A')]
    # find loops and then just lcm?
    loops = [find_loop_length(network, cur, instr) for cur in curs]
    # too low: 35447012203
    return math.lcm(*loops) * len(instr)  # initially forgot each instr is a "step"


def find_loop_length(network, start, instr):
    tort, hare = start, start
    i = 0
    # Thought I would need 'zends' but he was nice and had the loop happen AT the 'Z'
    # zends = []
    while True:
        i += 1
        for inst in instr:
            tort = network[tort][0 if inst == 'L' else 1]
        # if tort.endswith('Z'):
        #     zends.append(i)

        for inst in instr:
            hare = network[hare][0 if inst == 'L' else 1]
        for inst in instr:
            hare = network[hare][0 if inst == 'L' else 1]

        if tort == hare:
            return i  # , zends


if __name__ == '__main__':
    main()
