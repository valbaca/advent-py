from collections import defaultdict

from advent import elf

# Not clean but the dep graph not being a DAG is tricky
# Still, was able to sorta brute-force it


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


def parse(lines):
    ordering = defaultdict(set)
    updates = []
    for line in lines:
        if "|" in line:
            a,b = elf.septoi(line)
            ordering[b].add(a)
        elif "," in line:
            updates.append(list(elf.septoi(line)))
        else:
            raise Exception("Unrecognized line: " + line)
    return ordering, updates


class Rules:
    def __init__(self, lines):
        self.ordering, self.updates = parse(lines)


    def valid(self, curr, rest, seen=None):
        # seen is necessary bc the tree isn't a DAG
        if seen is None:
            seen = {curr}
        elif curr in seen:
            return True
        deps = self.ordering[curr]
        if len(deps & rest) > 0:
            return False
        for dep in deps:
            seen.add(dep)
            sub_valid = self.valid(dep, rest, seen)
            if not sub_valid:
                return False
        return True

    def make_valid(self, xs):
        out = []
        while xs:
            for i in range(len(xs)):
                curr = xs[i]
                if self.valid(curr, set(xs)):
                    out.append(curr)
            for a in out:
                if a in xs:
                    xs.remove(a)
        return out


def part1(lines):
    rules = Rules(lines)
    res = 0
    for update in rules.updates:
        for i in range(len(update)):
            curr = update[i]
            rest = set(update[i+1:])
            if not rules.valid(curr, rest):
                break
        else:
            res += update[len(update)//2]
    return res

def part2(lines):
    rules = Rules(lines)
    res = 0
    for update in rules.updates:
        for i in range(len(update)):
            curr = update[i]
            rest = set(update[i+1:])
            if not rules.valid(curr, rest):
                fixed = rules.make_valid(update.copy())
                res += fixed[len(fixed) // 2]
                break
    return res


if __name__ == '__main__':
    main()
