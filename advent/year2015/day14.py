from advent.elf import clamp, read_lines, septoi
"""
TIL: max accepts a function, so you can do "max_by", which can be o(n) rather than sorting
"""

class Deer:
    def __init__(self, line):
        # Rudolph can fly 22 km/s for 8 seconds, but then must rest for 165 seconds.
        s = septoi(line)
        # self.name = s[0]
        nums = [n for n in s if isinstance(n, int)] # rather than dealing with indexes
        self.speed, self.stamina, self.rest = nums
        self.cycle = self.stamina + self.rest
        self.dist = self.speed * self.stamina
        self.points = 0
    
    def calc_dist(self, time):
        dist = 0
        if time >= self.cycle:
            fullCycles, time = divmod(time, self.cycle)
            dist = fullCycles * self.dist
        time = clamp(time, 0, self.stamina)
        return dist + time * self.speed
        

def part1(input):
    deers = [Deer(line) for line in input]
    return max(deer.calc_dist(2503) for deer in deers)


def part2(input):
    deers = [Deer(line) for line in input]
    for i in range(1, 2503+1):
        deer_dists = [(deer, deer.calc_dist(i)) for deer in deers]
        mx_deer, _ = max(deer_dists, key=lambda x: x[1])
        mx_deer.points += 1
    return max(deer.points for deer in deers)


if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
