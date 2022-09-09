from collections import defaultdict
from itertools import permutations, product
from advent import elf

"""
TIL: persistence pays off. I was *really* close to giving up and skipping this one.
This honestly took a few days of thinking over and even then, I'm not happy with the slow,
brute-force-like solution.

Takes ~2mins to run the real input.
Certainly room for major improvements on this one, but I'm just tired of this problem at this point.
"""


THRESHOLD = 12

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 & 2 (test):")
    print(soln(test_lines))
    print("Part 1 & 2:")
    print(soln(lines))

def soln(lines):
    scs = parse_scanners(lines) # scs = scanners
    left_map = defaultdict(dict) # left_map[a][b] = offset to go from a<-b
    right_map = defaultdict(dict) # right_map[c][d] = offset to go from c->d

    for sci, sc in enumerate(scs):
        for o_sci, osc in enumerate(scs):
            if sci == o_sci:
                continue
            offset = find_offset(sc, osc)
            if offset:
                # print(sci, o_sci, offset) # uncomment to show progress...
                left_map[sci][o_sci] = offset # to get to sci, from o_sci, use offset
                right_map[o_sci][sci] = offset # to get from o_sci to sci, use offset
    
    # My terrible DAG builder. There are few than 30 scanners so this is fast enough
    dist_from_zero = {}
    queue = [(0,0)] # (scanner_number, dist_from_zero)
    while len(queue) > 0:
        curr, dist = queue.pop()
        if curr in dist_from_zero and dist_from_zero[curr] < dist:
            continue
        for nxt in left_map[curr].keys():
            queue.append((nxt, dist+1))
        dist_from_zero[curr] = dist

    # AND finally, getting the answer
    points = set()
    origins = []
    for i, sc in enumerate(scs):
        sc_points, origin = reduce_to_zero(i, sc, right_map, dist_from_zero)
        points.update(sc_points)
        origins.append(origin)
    return len(points), part2(origins)

def reduce_to_zero(start_i, sc, right_map, dist_from_zero):
    path = []
    curr = start_i
    curr_dist = dist_from_zero[start_i]
    while curr_dist > 0:
        nxt_map = None
        for maps in right_map[curr]:
            if dist_from_zero[maps] < curr_dist:
                curr_dist = dist_from_zero[maps]
                nxt_map = maps
        if nxt_map is None:
            raise RuntimeError(f"No path 'down' from {curr}")
        path.append(nxt_map)
        curr = nxt_map
    curr = start_i
    curr_sc = sc
    origin = [0,0,0]
    for nxt_map in path:
        orig, roti = right_map[curr][nxt_map]
        nxt_sc = [apply_offset(p, orig, roti) for p in curr_sc]
        origin = apply_offset(origin, orig, roti)
        curr = nxt_map
        curr_sc = nxt_sc
    return setify(curr_sc), origin


def tuplify(lst_of_points):
    return [tuple(e) for e in lst_of_points]

def setify(points):
    return set(tuplify(points))

def apply_offset(p, origin, roti):
    return add_points(origin, ROTATIONS[roti](p))

def parse_scanners(lines):
    scs = []
    for line in lines:
        if "scanner" in line:
            scs.append([])
            continue
        scs[-1].append(elf.septoi(line))
    return scs

def create_rot(pos, sgn):
    ia, ib, ic = pos
    sa, sb, sc = sgn
    return lambda p: [sa * p[ia], sb * p[ib], sc * p[ic]]

def gen_rotations():
    out = []
    # BAD! This creates 2x more rotations than necessary
    for pos in permutations(range(3), 3):
        for sgn in product([1,-1], repeat=3):
            out.append(create_rot(pos, sgn))
    return out

ROTATIONS = gen_rotations()

# BAD: There has to be a better way than this.
def find_offset(sa, sb):  # scanner a & b
    for a in sa:
        adiffs = [diff_points(othera, a) for othera in sa]
        adiffset = setify(adiffs)
        for rot_i, rot in enumerate(ROTATIONS):
            rot_sb = [rot(b) for b in sb]
            for b in rot_sb:
                matches = 0
                for otherb in rot_sb:
                    bd = diff_points(otherb, b)
                    if tuple(bd) in adiffset:
                        matches += 1
                        if matches >= THRESHOLD:
                            return diff_points(a, b), rot_i

def diff_points(n, m):
    return [n[0]-m[0], n[1]-m[1], n[2]-m[2]]

def add_points(n, m):
    return [n[0]+m[0], n[1]+m[1], n[2]+m[2]]

def part2(origins):
    mx = -1
    for o1 in origins:
        for o2 in origins:
            mx = max(mx, manh3d(o1, o2))
    return mx

def manh3d(a, b):
    return max(a[0] - b[0], b[0] - a[0]) + max(a[1] - b[1], b[1] - a[1]) + max(a[2] - b[2], b[2] - a[2])

if __name__ == '__main__':
    main()
