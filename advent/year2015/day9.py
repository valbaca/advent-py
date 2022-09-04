from collections import defaultdict
from advent.elf import read_lines, safe_atoi, septoi

# (plan: list, left: set, dist: int)

def part1(input):
    plans = calc_plans(input)
    plans.sort(key=lambda plan: plan[2])
    return plans[0][2]

def calc_plans(input):
    distances = defaultdict(dict) # one to one
    for line in input:
        a, _, b, d = septoi(line)
        distances[a][b] = d
        distances[b][a] = d
    locs = distances.keys()
    plans = []
    for loc in locs:
        plan = [loc]
        left = set(locs)
        left.remove(loc)
        plans.extend(go_dist(distances, plan, left, 0))
    return plans

def go_dist(distances, plan, left, dist):
    if len(left) == 0:
        return [(plan, left, dist)]
    plans = []
    for dest in left:
        sub_plan = [*plan, dest] # realized we don't actually need to track the full plan
        sub_left = left.copy()
        sub_left.remove(dest)
        plans.extend(go_dist(distances, sub_plan, sub_left, dist + distances[plan[-1]][dest]))
    return plans

def part2(input):
    plans = calc_plans(input)
    plans.sort(key=lambda plan: plan[2], reverse=True)
    return plans[0][2]

if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
