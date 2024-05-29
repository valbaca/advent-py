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
    x: int;
    y: int;
    size: int;
    used: int;
    avail: int

    def position(self):
        return (self.x, self.y)

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


def parse_node(line: str):
    return Node(*elf.septoi(line, r"[^0-9]")[:5])


def viable_pair(a, b):
    return 0 < a.used <= b.avail


def part1(lines):
    nodes = {node.position(): node for line in lines[2:] if (node := parse_node(line))}
    pos_list = list(nodes.keys())
    count = 0
    for i, pos in enumerate(pos_list):
        rest = pos_list[i + 1:]
        for other in rest:
            count += 1 if viable_pair(nodes[pos], nodes[other]) else 0
            count += 1 if viable_pair(nodes[other], nodes[pos]) else 0
    return count


def print_grid(nodes, src, tgt):
    pos_list = list(sorted(list(nodes.keys())))
    x = None  # x is the transfer node
    w = None  # w is the start/end wall node
    for i, pos in enumerate(pos_list):
        # if pos[1] == 0:
        #     print()
        rest = pos_list[:]
        pos_count = 0
        for other in rest:
            if pos == other:
                continue
            pos_count += 1 if viable_pair(nodes[pos], nodes[other]) else 0
            pos_count += 1 if viable_pair(nodes[other], nodes[pos]) else 0
        ch = '.'
        if pos == src:
            ch = 'S'
        elif pos == tgt:
            ch = 'T'
        elif not pos_count:
            ch = '#'
            if not w:
                w = nodes[(pos[0] - 1, pos[1])]
                ch = '^'
        elif viable_pair(nodes[src], nodes[pos]):
            ch = 'X'
            x = nodes[pos]
        # print(ch, end='')
    # print()
    src_node = nodes[src]
    # print('W=', w)
    # print('X=', x)
    # print('S=', src_node)
    dist = (x - w)
    dist += abs(w.x - src_node.x) + w.y
    dist += (5 * (src_node.x - 1))
    return dist


# After being stumped on this for a very long time, peeked online and it's not meant to be solved in the general case
def part2(lines):
    nodes = {node.position(): node for line in lines[2:] if (node := parse_node(line))}
    pos_list = list(nodes.keys())
    src = max(pos[0] for pos in pos_list), 0
    return print_grid(nodes, src, (0, 0))


if __name__ == '__main__':
    main()
