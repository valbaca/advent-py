from dataclasses import dataclass

from advent import elf


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))

@dataclass
class Node:
    # Filesystem              Size  Used  Avail  Use%
    # /dev/grid/node-x0-y0     89T   65T    24T   73%
    x: int; y: int; size: int; used: int; avail: int
    def position(self):
        return (self.x, self.y)

def parse_node(line: str):
    return Node(*elf.septoi(line, r"[^0-9]")[:5])

def viable_pair(a, b):
    return 0 < a.used <= b.avail

def part1(lines):
    nodes = {node.position(): node for line in lines[2:] if (node := parse_node(line))}
    pos_list = list(nodes.keys())
    count = 0
    for i, pos in enumerate(pos_list):
        rest = pos_list[i+1:]
        for other in rest:
            count += 1 if viable_pair(nodes[pos], nodes[other]) else 0
            count += 1 if viable_pair(nodes[other], nodes[pos]) else 0
    return count


def part2(lines):
    ...


if __name__ == '__main__':
    main()
