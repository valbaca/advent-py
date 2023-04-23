import heapq
import string
from collections import defaultdict, deque
from dataclasses import dataclass
from heapq import heappush, heappop

from advent import elf


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
    zeroes = [ch for ch in lines[2] if ch in string.ascii_letters]
    ones = [ch for ch in lines[3] if ch in string.ascii_letters]
    return list(zip(zeroes, ["A0", "B0", "C0", "D0"])) + list(zip(ones, ["A1", "B1", "C1", "D1"]))


energy = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


@dataclass(order=True)
class State:
    energy: int
    poss: list

    def pos_map(self):
        return pos_map(self.poss)

    def solved(self):
        for (name, pos) in self.poss:
            if name != pos[0]:
                return False
        return True


def pos_map(poss):
    return {pos: ele for (ele, pos) in poss}


def is_pos_in_hall(pos):
    return pos[0] not in "ABCD"


def is_pos_in_doorway(pos):
    return pos in ["2", "4", "6", "8"]


def is_pos_in_room(pos):
    return pos[0] in "ABCD"


def is_pos_outer_room(pos):
    return is_pos_in_room(pos) and pos[1] == '0'


def is_pos_inner_room(pos):
    return is_pos_in_room(pos) and pos[1] == '1'


def get_other_room(pos):
    if is_pos_inner_room(pos):
        return pos[0] + '0'
    elif is_pos_in_room:
        return pos[0] + '1'
    else:
        raise AssertionError()


def part1(lines):
    graph = defaultdict(list)
    for x in range(0, 11):
        xstr = str(x)
        if x - 1 >= 0:
            graph[xstr] += str(x - 1)
        if x + 1 < 11:
            graph[xstr].append(str(x + 1))
    graph["2"] += ["A0"]
    graph["A0"] += ["2", "A1"]
    graph["A1"] += ["A0"]

    graph["4"] += ["B0"]
    graph["B0"] += ["4", "B1"]
    graph["B1"] += ["B0"]

    graph["6"] += ["C0"]
    graph["C0"] += ["6", "C1"]
    graph["C1"] += ["C0"]

    graph["8"] += ["D0"]
    graph["D0"] += ["8", "D1"]
    graph["D1"] += ["D0"]

    def find_possibilities(state, min_found):
        out = []
        pm = state.pos_map()
        occupied = pm.keys()
        for (idx, (name, src)) in enumerate(state.poss):
            ends = {}  # end positions -> energy to go there
            nodes = deque([(p, energy[name], [src]) for p in graph[src] if p not in occupied])  # (dest pos, nrg, path)
            while nodes:
                # `continue` when you cannot even travel to/through
                # `is_end` is only True if we can stop/terminate in position
                dst, nrg, path = nodes.popleft()
                if dst in occupied or dst in path:
                    continue
                is_end = False
                prev = path[-1]
                if is_pos_in_doorway(prev) and is_pos_outer_room(dst):
                    # entering a room
                    if dst[0] != name[0]:
                        continue  # wrong room
                    # right room
                    inner_room = dst[0] + '1'
                    inner_occ = pm.get(inner_room)
                    if inner_occ is None:  # right room, but inner is empty, this is fine but cannot stop here
                        is_end = False  # redundant
                    elif inner_occ[0] == dst[0]:  # inner has correct occupant, settle in
                        is_end = True
                    else:  # right room, but inner occupant is wrong, cannot enter the room
                        continue
                elif is_pos_inner_room(dst):
                    # can (and must!) settle if inner room matches
                    if dst[0] == name[0]:
                        is_end = True
                    else:
                        continue
                elif is_pos_outer_room(prev) and is_pos_in_doorway(dst):
                    # don't leave room if it's fully settled, outer and inner
                    if prev[0] == name[0] and pm.get(prev[0] + '1') == name[0]:
                        continue
                elif is_pos_inner_room(prev):
                    # don't leave inner room if matches
                    if prev[0] == name[0]:
                        continue

                # can settle in hallway (but not doorway) if started from room
                if is_pos_in_room(src) and is_pos_in_hall(dst) and not is_pos_in_doorway(dst):
                    is_end = True
                dst_path = path[:]  # ABSOLUTELY CRUCIAL to clone the list...don't ask how much time was wasted
                dst_path.append(dst)
                nodes.extend(
                    [(p, nrg + energy[name], dst_path) for p in graph[dst] if p not in occupied and p not in dst_path])
                if is_end:
                    if dst not in ends or ends[dst] > nrg:
                        ends[dst] = nrg
            for (new_pos, nrg) in ends.items():
                new_poss = state.poss.copy()
                new_poss[idx] = (name, new_pos)
                new_nrg = state.energy + nrg
                if new_nrg < min_found:
                    out.append(State(new_nrg, new_poss))
        return out



    start_poss = parse(lines)
    min_found = 20000  # semi-arbitrary upper-limit
    pq = [State(0, start_poss)]
    all_seen = {}
    while pq:
        state = heappop(pq)
        # print(state)
        poss_tuple = tuple(state.poss)
        best_energy = all_seen.get(poss_tuple)
        if best_energy is None or best_energy > state.energy:
            all_seen[poss_tuple] = state.energy
        else:
            continue  # been here, done that
        if state.energy > min_found:
            continue
        if state.solved():
            if state.energy < min_found:
                min_found = state.energy
                # print(min_found)
                # pre_len = len(pq)
                pq = [s for s in pq if s.energy < min_found]
                heapq.heapify(pq)
                # print(f"re-heaped from {pre_len} to {len(pq)}")
            continue
        possibilities = find_possibilities(state, min_found)
        for poss in possibilities:
            heappush(pq, poss)
        # print(len(pq))
    return min_found


def part2(lines):
    ...


if __name__ == '__main__':
    main()
