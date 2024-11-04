import math
from typing import Self

from advent import elf
from advent.elf import septoi

"""
Had to lookup help for the second part on this one.
Based on the themes of this year, I figured it was related to cycles.
However, my attempts to find the cycles failed. I kept finding them at n=2 or otherwise
wrong numbers.

Yet again, @xavdid saves my butt.
At least for this one, I felt like I had a good idea of *what* I was looking for, I just
fumbled the last bit; which is fine for learning.

But overall, this was not my favorite puzzle. Not a fan of the ones where you find the "trick"
based on your particular input, and not all possible inputs.
Put these are pretty typical for late-month days.
"""

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    # print("Part 2 (test):")
    # print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


class Node:
    pulses = {True: 0, False: 0}

    def __init__(self, line: str):
        splits = septoi(line)
        self.id = splits[0]
        self.type = line[0]  # % or & or 'b'
        self.dsts = splits[2:]
        if self.type == '%':
            self.state = False
        elif self.type == '&':
            self.inputs = {}

    def __str__(self):
        if self.type != "&" and self.type != "%":
            return self.id
        if self.type == '%':
            return f"{self.type}{self.id}={self.state}"
        if self.type == '&':
            return f"{self.type}{self.id}=[{",".join(self.inputs.keys())}]"
        return f"{self.type}{self.id}=?"

    def add_input(self, source: str):
        assert self.type == '&'
        self.inputs[source] = False

    @classmethod
    def reset_pulses(cls):
        cls.pulses = {True: 0, False: 0}

    def pulse(self, source: Self, signal: bool) -> list[tuple[Self, str, bool]]:
        Node.pulses[signal] += 1
        if self.type == '%':
            if signal:
                return []
            else:
                self.state = not self.state
                return [(self, d, self.state) for d in self.dsts]
        elif self.type == '&':
            self.inputs[source.id] = signal
            out = not all(self.inputs.values())
            return [(self, d, out) for d in self.dsts]
        else:
            return [(self, d, signal) for d in self.dsts]


def part1(lines):
    Node.reset_pulses()
    nodes = [Node(line) for line in lines]
    rxs = [n for n in nodes if n.type == '&']
    for rx in rxs:
        for source in nodes:
            if rx.id in source.dsts:
                rx.add_input(source.id)
    source_ids = {n.id for n in nodes}
    dest_ids = {dest for n in nodes for dest in n.dsts}
    for dest_only in dest_ids - source_ids:
        nodes.append(Node(dest_only))
    system = {n.id: n for n in nodes}

    for _ in range(1000):
        q = [("Button", "broadcaster", False)]
        while q:
            src, dst, signal = q.pop(0)
            if dst_node := system.get(dst):
                q += dst_node.pulse(src, signal)
            else:
                raise RuntimeError("dst not found: " + dst)
    return Node.pulses[True] * Node.pulses[False]


def part2(lines):
    # copied from part1
    Node.reset_pulses()
    nodes = [Node(line) for line in lines]
    rxs = [n for n in nodes if n.type == '&']
    for rx in rxs:
        for source in nodes:
            if rx.id in source.dsts:
                rx.add_input(source.id)
    source_ids = {n.id for n in nodes}
    dest_ids = {dest for n in nodes for dest in n.dsts}
    for dest_only in dest_ids - source_ids:
        nodes.append(Node(dest_only))
    system = {n.id: n for n in nodes}

    n = 1
    ends = ['sg', 'lm', 'dh', 'db']  # manually found using debugger
    detected_cycles = {}
    while True:
        q = [(None, "broadcaster", False)]
        while q:
            src, dst, signal = q.pop(0)
            if src and src.id in ends and signal == True:
                print(f"high to {src.id} at {n=}")
                if src.id not in detected_cycles:
                    detected_cycles[src.id] = n

            q += system.get(dst).pulse(src, signal)
            if all(end in detected_cycles for end in ends):
                return math.lcm(*detected_cycles.values())
        n += 1


if __name__ == '__main__':
    main()
