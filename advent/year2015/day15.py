import math
from advent.elf import only_ints, product, read_lines, septoi

class Ingr:
    def __init__(self, line):
        self.vals = only_ints(septoi(line))

def part1(input):
    ings = [Ingr(line) for line in input]
    return optimize(ings, get_score)

def get_score(ms): # ms = measurements, (tsp, ingredient)
    ing = ms[0][1]
    sums = [0] * (len(ing.vals)-1) # skip calories
    for tsp, ing in ms:
        for i in range(len(sums)):
            sums[i] += (tsp * ing.vals[i])
    for s in sums:
        if s <= 0:
            return 0
    return product(sums)

def optimize(ings, scoreFn):
    return opt_recur(ings, 100, [], scoreFn)

def opt_recur(ings, left, drink, scoreFn):
    if len(ings) == 1:
        drink.append((left, ings[0]))
        return scoreFn(drink)
    mx = 0
    for i in range(0, left+1):
        d = drink[::]
        d.append((i, ings[0]))
        mx = max(mx, opt_recur(ings[1:], left-i, d, scoreFn))
    return mx

target_cal = None

def part2(input):
    ings = [Ingr(line) for line in input]
    global target_cal
    target_cal = 500
    return optimize(ings, get_score_cal)

def get_score_cal(ms): # ms = measurements, (tsp, ingredient)
    ing = ms[0][1]
    sums = [0] * len(ing.vals)
    for tsp, ing in ms:
        for i in range(len(sums)):
            sums[i] += (tsp * ing.vals[i])
    if sums[-1] != target_cal:
        return 0
    for s in sums:
        if s <= 0:
            return 0
    return product(sums[:-1])

if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
