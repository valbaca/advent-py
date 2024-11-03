import re
from typing import Self

from advent import elf
from advent.elf import product

"""
This one was challenging but just the right amount. Part 1 was super easy, like a day 1 problem.
Part 2 was tricky to keep in my head. I knew what I wanted to do at a high level, but the whole instructions and xmas
part made it a bit trickier.

This was definitely one where breaking it down into parts/classes helped a lot.
I tested the SRange class alone, I knew I needed to bc of off-by-one errors.
Then moved onto the Part class, which just does SRange MORE.

Finally, the `acceptable` function was one harder to imagine until I just started coding.
Thinking with Monads (i.e. List) really helped there. Just returning lists (empty or not) made it easy to combine with
the DFS it executes.

This code isn't succinct but I'm proud that Part 2 worked on the first try! (excluding "unit" testing)
"""

def main():
    test_lines = elf.lines_blank_grouped(elf.test_file(__file__))
    lines = elf.lines_blank_grouped(elf.in_file(__file__))
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(groups):
    workflows_lines, parts_lines = groups[0], groups[1]
    workflows = Workflows(workflows_lines)
    parts = [parse_part(part_line) for part_line in parts_lines]
    return sum(score_part(part) for part in parts if workflows.accept(part))


class Workflows:
    def __init__(self, lines):
        self.workflows = {}
        for line in lines:
            w_id, w_fn = Workflows.parse_workflow_line(self.workflows, line)
            self.workflows[w_id] = w_fn

    def accept(self, part):
        return self.workflows["in"](part) == "A"

    @staticmethod
    def parse_workflow_line(workflows, line: str):
        id = line[:line.index("{")]
        instructions = line[line.index("{") + 1:-1].split(",")

        def work(part):
            for ins in instructions:
                res = None
                if ":" in ins:
                    check, dest = ins.split(":")
                    if "<" in check:
                        prop, comp = check.split("<")
                        if part[prop] < int(comp):
                            res = dest
                    elif ">" in check:
                        prop, comp = check.split(">")
                        if part[prop] > int(comp):
                            res = dest
                else:
                    res = ins
                if res == "A" or res == "R":
                    return res
                elif res:
                    return workflows[res](part)  # default

        return id, work


def parse_part(line: str):
    part = {}
    splits = line[1:-1].split(",")
    for s in splits:
        k, v = s.split("=")
        part[k] = int(v)
    return part


def score_part(part: dict):
    return sum(part.values())


########################################################################################################################
# Basically just starting over for part 2

class SRange:
    """Splitable Range: when 'asked' a comparison, returns two ranges where the comparison is true and false"""

    def __init__(self, start, end):
        assert start < end
        self.start = start
        self.end = end  # exclusive

    def __repr__(self):
        return f"[{self.start},{self.end})"

    def __contains__(self, item):
        return self.start <= item < self.end

    def compare(self, lt_gt: str, n: int) -> tuple[Self | None, Self | None]:
        """Return a pair of SRanges where the values for comparison is true and false"""
        if lt_gt == "<":
            if n <= self.start:
                return None, self # all above
            elif n >= self.end:
                return self, None # all below
            else:
                return SRange(self.start, n), SRange(n, self.end)
        else:
            if n < self.start:
                return self, None
            elif n >= self.end:
                return self, None
            else:
                return SRange(n + 1, self.end), SRange(self.start, n + 1)

# did a spot test of the srange class to squash the off-by-one bugs
def test_srange():
    sr = SRange(0, 100)
    for x in range(0, 110, 10):
        for c in ['<', '>']:
            print(f"{c}{x} => {sr.compare(c, x)}")


class Part:
    def __init__(self, xmas=None):
        if xmas is None:
            self.xmas = {
                'x': SRange(1, 4000 + 1),
                'm': SRange(1, 4000 + 1),
                'a': SRange(1, 4000 + 1),
                's': SRange(1, 4000 + 1),
            }
        else:
            self.xmas = xmas # type: dict[str, SRange]

    def score(self):
        return product(x.end - x.start for x in self.xmas.values())

    def compare(self, xmas: str, lt_gt: str, n: int) -> tuple[Self | None, Self | None]:
        xmas_range = self.xmas[xmas]
        true_xmas_range, false_xmas_range = xmas_range.compare(lt_gt, n)
        if true_xmas_range is None:
            return None, self
        elif false_xmas_range is None:
            return self, None
        else:
            true_xmas = self.xmas.copy() # kind of miss clojure here...
            true_xmas[xmas] = true_xmas_range
            false_xmas = self.xmas.copy()
            false_xmas[xmas] = false_xmas_range
            return Part(true_xmas), Part(false_xmas)


def part2(groups):
    workflow_lines = groups[0]
    workflows = {}

    def parse_instruction(istr):
        if ":" in istr:
            check, dest = istr.split(":")
            xmas, n = re.split(r"[<>]", check)
            lt_gt = "<" if "<" in check else ">"
            return xmas, lt_gt, int(n), dest
        else:
            return istr # GOTO instruction

    for line in workflow_lines:
        id = line[:line.index("{")]
        instructions_strs = line[line.index("{") + 1:-1].split(",")
        workflows[id] = [parse_instruction(i) for i in instructions_strs]

    def acceptable(part: Part | None, iid: str = "in") -> list[Part]:
        """Using DFS and splitting the parts, returns a list of acceptable parts"""
        if part is None: # easier to handle the empty parts this way than below
            return []
        if iid == "A":
            return [part]
        elif iid == "R":
            return []
        wins = workflows[iid]  # workflow instructions
        out = []
        # This part(!) is tricky, but it's basically DFS
        for w in wins:
            if isinstance(w, str):
                return out + acceptable(part, w)  # execute GOTO, last instruction so we're done
            xmas, lt_gt, n, dest = w
            true_part, false_part = part.compare(xmas, lt_gt, n) # split the universe
            out += acceptable(true_part, dest) # collect DFS results
            # Only the `false_part` filters into the next instruction
            if false_part is None:
                return out
            part = false_part
        raise RuntimeError() # should've hit the GOTO

    return sum(part.score() for part in acceptable(Part()))


if __name__ == '__main__':
    main()
