import re

from advent import elf

'''
This was a cute one. Literally creating a hash and hashmap from scratch.
Granted, I kind of cheat by using an *actual* hash map instead of the array + linked list you're "supposed" to use.
~~Might be cute to go back and do this without using an actual hashmap~~

Update: did it, it was trivial. Python is great that way.
'''


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


def hsh(s):
    i = 0
    for ch in s:
        i += ord(ch)
        i *= 17
    return i % 256 # put mod at end b/c it's python


def part1(lines):
    return sum(hsh(s) for s in lines[0].split(","))


class Box:
    def __init__(self, n):
        self.n = n
        self.lenses = [] # lenses are basically a linked list

    def remove(self, key):
        for i, (elabel, _) in enumerate(self.lenses):
            if elabel == key:
                del self.lenses[i]
                return

    def put(self, key, value):
        for i, (elabel, _) in enumerate(self.lenses):
            if elabel == key:
                self.lenses[i] = (key, value)
                return
        self.lenses.append((key, value))

    def __repr__(self):
        return f"Box {self.n}: {self.lenses}"


def part2(lines):
    hm = [Box(n) for n in range(256)]
    regex = re.compile(r"[=-]")
    for s in lines[0].split(","):
        label, *value = elf.septoi(s, regex)
        h = hsh(label)
        box = hm[h]
        if '-' in s:
            box.remove(label)
        elif '=' in s:
            box.put(label, value[0])
        hm[h] = box

    return sum(
        (box.n + 1) * (lens_i + 1) * lens[1]
        for box_num, box in enumerate(hm)
        for lens_i, lens in enumerate(box.lenses)
    )




if __name__ == '__main__':
    main()
