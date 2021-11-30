import advent.elf as elf
"""TIL no ++ or -- in Python
enumerate to loop with index (more like C-style for-loop)
"""
def part1(s):
    """Returns which floor Santa ends up on."""
    total = 0
    for c in s:
        if c == '(':
            total += 1
        elif c == ')':
            total -= 1
    return total

def part2(s):
    """Return the pos of the command that puts Santa on -1"""
    total = 0
    for pos, c in enumerate(s, start=1):
        if c == '(':
            total += 1
        elif c == ')':
            total -= 1
        if total == -1:
            return pos
    return -1

if __name__ == '__main__':
    print(part1(elf.read_lines(__file__)[0]))
    print(part2(elf.read_lines(__file__)[0]))