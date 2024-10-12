from advent import elf


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    # print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


class Node:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.left = None
        self.right = None

    def insert(self, node):
        na, nb = node.a, node.b
        if self.a <= na <= nb <= self.b:
            return  # already contained
        # left, no overlap
        elif nb < self.a:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)
        # left, overlap
        elif na < self.a:
            self.a = min(self.a, na)
            self.b = max(self.b, nb)
        # right, no overlap
        elif na > self.b:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)
        # right, overlap
        elif nb > self.b:
            self.a = min(self.a, na)
            self.b = max(self.b, nb)
        else:
            raise Exception(f"fucky wucky {self} {node}")

    def contains(self, i):
        if self.a <= i <= self.b:
            return True
        if i < self.a and self.left is not None:
            return self.left.contains(i)
        if i > self.b and self.right is not None:
            return self.right.contains(i)
        return False

    def size_of(self, overnode):
        if overnode.b < self.a:
            if not self.left:
                return overnode.b - overnode.a + 1  # no overlap at all
            return self.left.size_of(overnode)
        if overnode.a > self.b and not self.right:
            if not self.right:
                return overnode.b - overnode.a + 1  # no overlap at all
            return self.right.size_of(overnode)

        total = 0
        if overnode.a < self.a:
            if not self.left:
                total += (self.a - overnode.a)
            else:
                total += self.left.size_of(Node(overnode.a, self.a-1))

        if overnode.b > self.b:
            if not self.right:
                total += (overnode.b - self.b)
            else:
                total += self.right.size_of(Node(self.b+1, overnode.b))
        return total


def part1(lines):
    pairs = [elf.septoi(line, '-') for line in lines]
    root = Node(pairs[0][0], pairs[0][1])
    for a, b in pairs[1:]:
        root.insert(Node(a, b))
    for i in range(4294967295):
        if not root.contains(i):
            return i
    return None

    # lines = ["5-8", "0-2", "4-7"]
    # lines.sort(key=lambda x: elf.septoi(x, r"[-]")[0])

    # lines = ",".join(lines)
    # print(complement_int_list(lines, range_start=0, range_end=4294967295))
    # return parse_int_list(lines)


def part2(lines):
    # lines = ["5-8", "0-2", "4-7"]
    pairs = [elf.septoi(line, '-') for line in lines]
    root = Node(pairs[0][0], pairs[0][1])
    for a, b in pairs[1:]:
        root.insert(Node(a, b))
    # return root.size_of(Node(0, 9))
    return root.size_of(Node(0, 4294967295))


if __name__ == '__main__':
    main()
