from advent import elf

"""
TIL: Pencil and paper (or Apple Pencil and iPad) and patience is all you need.
Oh, and don't make stupid algebra errors.
"""
def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    # print("Part 1 (test):")
    # print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    # print("Part 2 (test):")
    # print(part2(test_lines))
    # print("Part 2:")
    # print(part2(lines))

def alu(vrs: dict, s: str, inp: list):
    args = s.split(" ")
    op = args[0]
    a = args[1]
    if op == "inp":
        vrs[a] = int(inp.pop())
    else:
        b = elf.safe_atoi(args[2])
        if isinstance(b, str):
            b = vrs[b]

        if op == "add":
            vrs[a] = vrs[a] + b
        elif op == "mul":
            vrs[a] = vrs[a] * b
        elif op == "div":
            vrs[a] = vrs[a] // b
        elif op == "mod":
            vrs[a] = vrs[a] % b
        elif op == "eql":
            vrs[a] = 1 if vrs[a] == b else 0

def run_alu(lines, s: str, z=0):
    inp = list(s)
    vrs = {"w": 0, "x": 0, "y": 0, "z": z}
    for line in lines:
        alu(vrs, line, inp)
        # print(vrs)
    return vrs["z"]



def part1(lines):
    chunks = []
    for line in lines:
        if line.startswith("inp"):
            chunks.append([])
        chunks[-1].append(line)
    wh = "94992994195998"  # highest

    ws = "21191861151161"  # lowest
    #     321_9876543210   # digits
    z = 0
    for ci, chunk in enumerate(chunks[:]):
        w = ws[ci]
        print(f"Digit {13 - ci} w={w}")
        z_res = run_alu(chunk, w, z)
        z = z_res
        print(f"z={z} z/26={z//26} z%26={z%26}")

def part2(lines):
    ...


if __name__ == '__main__':
    main()
