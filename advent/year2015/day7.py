from advent.elf import read_lines, septoi

class Wire:
    WIRES = {}
    def __init__(self, s):
        self.s = s
        self.splits = septoi(s, r"[ >-]")
        self.id = self.splits[-1]
        self.sig_val = None # signal value
        Wire.WIRES[self.id] = self

    def signal(self) -> int:
        self.sig_val = self.sig_val or self.calc_sign()
        return self.sig_val

    def calc_sign(self):
        if "AND" in self.splits:
            return sig(self.splits[0]) & sig(self.splits[2])
        elif "OR" in self.splits:
            return sig(self.splits[0]) | sig(self.splits[2])
        elif "LSHIFT" in self.splits:
            return sig(self.splits[0]) << sig(self.splits[2])
        elif "RSHIFT" in self.splits:
            return sig(self.splits[0]) >> sig(self.splits[2])
        elif "NOT" in self.splits:
            return (~sig(self.splits[1])) & 0xFFFF  # to keep to [0, 65535]
        return sig(self.splits[0])

    @staticmethod
    def sig(val) -> int:
        if isinstance(val, int):
            return val
        return Wire.WIRES[val].signal()

sig = Wire.sig

def part1(input):
    for line in input:
        Wire(line)
    return Wire.WIRES["a"].signal()


def part2(input):
    prev_a = part1(input)
    for line in input:
        Wire(line)
    Wire.WIRES["b"].sig_val = prev_a # hook in the prev value
    return Wire.WIRES["a"].signal()


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
