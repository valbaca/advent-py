from advent import elf

"""
This one was rough, nearly threw in the towel but thinking of using in-order traversal to get
the "left" and "right" numbers was what really solidified things.
I also avoided using a Box for whatever reason, ended up making things much much easier.
"""

def main():
    lines = elf.read_lines(__file__)
    print("Part 1:")
    print(part1(lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    pair = Pair.parse(lines[0])
    for line in lines[1:]:
        pair = Pair.add(pair, Pair.parse(line))
    return pair.magnitude()


def part2(lines):
    mx = 0
    length = len(lines)
    for i in range(length):
        for j in range(length):
            if i != j:
                si, sj = Pair.parse(lines[i]), Pair.parse(lines[j])
                mag = Pair.add(si, sj).magnitude()
                if mx < mag:
                    mx = mag
    return mx


class Box:
    def __init__(self, val):
        self.val = val
    
    def add_val(self, val):
        self.val += val

    def magnitude(self):
        return self.val
    
    def __str__(self):
        return f"{self.val}"

class Pair:
    def __init__(self, left, right):
        self.left, self.right = left, right

    def parse(s):
        if s[0] != '[':
            return Box(int(s))
        p = 0
        level = 0
        comma_pos = -1
        for c in s:
            if c == '[':
                level += 1
            elif c == ']':
                level -= 1
            elif c == ',' and level == 1:
                comma_pos = p
                break
            p += 1
        p = comma_pos
        return Pair(Pair.parse(s[1:p]), Pair.parse(s[p+1:-1]))
    

    def add(left, right):
        p = Pair(left, right)
        p.reduce()
        return p

    def reduce(self):
        while True:
            did_explode = self.try_explode()
            if did_explode:
                continue
            did_split = self.try_split()
            if did_split:
                continue
            return

    def try_explode(self):
        return self.try_explode_recur(self, [])

    def try_explode_recur(self, root, path):
        if len(path) == 3:
            if isinstance(self.left, Pair):
                exploding_left, exploding_right = self.left.left.val, self.left.right.val
                root.add_to_left_of(self.left.left, exploding_left)
                root.add_to_right_of(self.left.right, exploding_right)
                self.left = Box(0)
                return True
            elif isinstance(self.right, Pair):
                exploding_left, exploding_right = self.right.left.val, self.right.right.val
                root.add_to_left_of(self.right.left, exploding_left)
                root.add_to_right_of(self.right.right, exploding_right)
                self.right = Box(0)
                return True
        if isinstance(self.left, Pair):
            sub_exploded = self.left.try_explode_recur(root, [*path, 0])
            if sub_exploded:
                return True
        if isinstance(self.right, Pair):
            sub_exploded = self.right.try_explode_recur(root, [*path, 1])
            if sub_exploded:
                return True
        return False

    def in_order(self):
        ret = []
        if isinstance(self.left, Box):
            ret.append(self.left)
        else:
            ret.extend(self.left.in_order())
        if isinstance(self.right, Box):
            ret.append(self.right)
        else:
            ret.extend(self.right.in_order())
        return ret


    def add_to_offset(self, offset, mid, val):
        in_orders = self.in_order()
        idx = in_orders.index(mid)
        tgt_idx = idx + offset
        if 0 <= (tgt_idx) < len(in_orders):
            in_orders[tgt_idx].add_val(val)

    def add_to_left_of(self, mid, val):
        self.add_to_offset(-1, mid, val)

    def add_to_right_of(self, mid, val):
        self.add_to_offset(1, mid, val)

    def try_split(self):
        return self.try_split_recur()

    def try_split_recur(self):
        if isinstance(self.left, Box) and self.left.val >= 10:
            lval, rval = split_num(self.left.val)
            self.left = Pair(Box(lval), Box(rval))
            return True
        if isinstance(self.left, Pair):
            res = self.left.try_split_recur()
            if res:
                return True
        if isinstance(self.right, Box) and self.right.val >= 10:
            lval, rval = split_num(self.right.val)
            self.right = Pair(Box(lval), Box(rval))
            return True
        if isinstance(self.right, Pair):
            res = self.right.try_split_recur()
            if res:
                return True
        return False

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        
    def __str__(self):
        return f"[{self.left},{self.right}]"

    def __repr__(self):
        return f"[{self.left},{self.right}]"


def split_num(n):
    if elf.even(n):
        return (n // 2), (n // 2)
    else:
        return (n // 2) , ((n //2 )+ 1) # round down, round up

if __name__ == '__main__':
    main()
