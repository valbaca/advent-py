from collections import defaultdict

from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


class Swarm:
    def __init__(self):
        self.bots = defaultdict(list)
        self.outputs = {}
        self.instructions = {}

    def exec(self, bot_id):
        low_tgt, low_id, high_tgt, high_id = self.instructions[bot_id]
        low_val, high_val = sorted(self.bots[bot_id])
        if low_tgt == 'output':
            self.outputs[low_id] = low_val
        else:
            self.give_value_to_bot(low_val, low_id)
        if high_tgt == 'output':
            self.outputs[high_id] = high_val
        else:
            self.give_value_to_bot(high_val, high_id)

    def parse_instructions(self, s):
        # bot 2 gives low to bot 1 and high to bot 0
        ss = s.split(" ")
        _, bot_id, _, _, _, low_tgt, low_id, _, _, _, high_tgt, high_id = ss
        bot_id = int(bot_id)
        self.instructions[bot_id] = (low_tgt, int(low_id), high_tgt, int(high_id))
        if len(self.bots[bot_id]) == 2:
            self.exec(bot_id)

    def give_value_to_bot(self, value, bot_id):
        self.bots[bot_id].append(value)
        if len(self.bots[bot_id]) == 2 and bot_id in self.instructions:
            self.exec(bot_id)

    def parse_line(self, line):
        if line.startswith("value"):
            _, val, _, _, _, bot_id = line.split(" ")
            self.give_value_to_bot(int(val), int(bot_id))
        else:
            self.parse_instructions(line)


def part1(lines):
    swarm = Swarm()
    for line in lines:
        swarm.parse_line(line)
    # for bot_id in sorted(bots.keys()):
    #     print(f"Bot {bot_id}: {bots[bot_id]}")
    # for output_id in sorted(outputs.keys()):
    #     print(f"Output {output_id}: {outputs[output_id]}")
    for bot_id, values in swarm.bots.items():
        if 61 in values and 17 in values:
            return bot_id


def part2(lines):
    swarm = Swarm()
    for line in lines:
        swarm.parse_line(line)
    return swarm.outputs[0] * swarm.outputs[1] * swarm.outputs[2]


if __name__ == '__main__':
    main()
