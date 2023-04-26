import heapq
import os
import string
from collections import defaultdict, deque
from dataclasses import dataclass
from heapq import heappush, heappop

from advent import elf
"""
THIS ONE SUUUUCKED.
I seriously put this one off for half a year and even then it took two near-full days of attempts.

Python makes it easy to get started but also easy to get stuck with stupid bugs 
(like using a position where an element id was expected).

But mostly, this problem was just a huge pain. So glad I powered through it and solved it on my own though! 
"""

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

    def __str__(self):
        s = ""
        pm = self.pos_map()
        for i in range(11):
            s += pm.get(str(i), ".")
        s += "\n"
        for i in range(4):
            s += "  "
            for a in "ABCD":
                s += pm.get(a + str(i), ".")
                s += " "
            s += "\n"
        return s


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
    return is_pos_in_room(pos) and (pos[1] in "123")


def get_other_room(pos):
    if is_pos_inner_room(pos):
        return pos[0] + '0'
    elif is_pos_in_room:
        return pos[0] + '1'
    else:
        raise AssertionError()


def inner_room_empty():
    pass  # TODO


def travel_logic(node, name, pm):  # return (is_legal, is_end)
    dst, nrg, path = node
    if dst in pm or dst in path:
        return False, False
    is_end = False
    prev = path[-1]
    if is_pos_in_doorway(prev) and is_pos_outer_room(dst):
        # entering a room
        if dst[0] != name[0]:
            return False, False  # wrong room, cannot enter
        # right room
        inner_room = dst[0] + '1'
        inner_occ = pm.get(inner_room)
        if inner_occ is None:  # right room, but inner is empty, this is fine but just cannot stop here
            is_end = False  # redundant
        elif inner_occ[0] == dst[0]:  # inner has correct occupant, settle in
            is_end = True
        else:  # right room, but inner occupant is wrong, cannot enter the room
            return False, False
    elif is_pos_inner_room(dst):
        # can (and must!) settle if inner room matches
        if dst[0] == name[0]:
            is_end = True
        else:
            return False, False
    elif is_pos_outer_room(prev) and is_pos_in_doorway(dst):
        # don't leave room if it's fully settled, outer and inner
        if prev[0] == name[0] and pm.get(prev[0] + '1') == name[0]:
            return False, False
    elif is_pos_inner_room(prev):
        # don't leave inner room if matches
        if prev[0] == name[0]:
            return False, False

    src = path[0]
    # can settle in hallway (but not doorway) if started from room
    if is_pos_in_room(src) and is_pos_in_hall(dst) and not is_pos_in_doorway(dst):
        is_end = True
    return True, is_end


def find_possibilities(state, graph, part2=False):
    out = []
    pm = state.pos_map()
    for (idx, (name, src)) in enumerate(state.poss):
        ends = {}  # end positions -> energy to go there
        nodes = deque([(p, energy[name], [src]) for p in graph[src] if p not in pm])  # (dest pos, nrg, path)
        while nodes:
            # `continue` when you cannot even travel to/through
            # `is_end` is only True if we can stop/terminate in position
            node = nodes.popleft()
            dst, nrg, path = node
            is_legal, is_end = travel_logic2(node, name, pm) if part2 else travel_logic(node, name, pm)
            if is_legal:
                dst_path = path[:] + [dst]  # absolutely critical to clone the path list or it all breaks
                nodes.extend([(p, nrg + energy[name], dst_path)
                              for p in graph[dst]
                              if p not in pm and p not in dst_path])
                if is_end:
                    if dst not in ends or ends[dst] > nrg:
                        ends[dst] = nrg
        for (new_pos, nrg) in ends.items():
            new_poss = state.poss.copy()
            new_poss[idx] = (name, new_pos)
            new_nrg = state.energy + nrg
            out.append(State(new_nrg, new_poss))
    return out


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

    start_poss = parse(lines)
    min_found = 20000  # heuristic upper-limit
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
        possibilities = find_possibilities(state, graph)
        for poss in possibilities:
            heappush(pq, poss)
        # print(len(pq))
    return min_found


def part2(lines):
    graph = defaultdict(list)
    for x in range(0, 11):
        xstr = str(x)
        if x - 1 >= 0:
            graph[xstr] += str(x - 1)
        if x + 1 < 11:
            graph[xstr].append(str(x + 1))
    graph["2"] += ["A0"]
    graph["A0"] += ["2", "A1"]
    graph["A1"] += ["A0", "A2"]
    graph["A2"] += ["A1", "A3"]
    graph["A3"] += ["A2"]

    graph["4"] += ["B0"]
    graph["B0"] += ["4", "B1"]
    graph["B1"] += ["B0", "B2"]
    graph["B2"] += ["B1", "B3"]
    graph["B3"] += ["B2"]

    graph["6"] += ["C0"]
    graph["C0"] += ["6", "C1"]
    graph["C1"] += ["C0", "C2"]
    graph["C2"] += ["C1", "C3"]
    graph["C3"] += ["C2"]

    graph["8"] += ["D0"]
    graph["D0"] += ["8", "D1"]
    graph["D1"] += ["D0", "D2"]
    graph["D2"] += ["D1", "D3"]
    graph["D3"] += ["D2"]

    start_poss = parse2(lines)
    min_found = 100000  # heuristic upper-limit
    pq = [State(0, start_poss)]
    all_seen = {}
    while pq:
        state = heappop(pq)
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
        # print("Start state:")
        # print(state)
        possibilities = find_possibilities(state, graph, True)
        # print("Possibilities")
        for poss in possibilities:
            # print(poss)
            heappush(pq, poss)
        # print(len(pq))
    return min_found


def parse2(lines):
    zeroes = [ch for ch in lines[2] if ch in string.ascii_letters]
    ones = list("DCBA")
    twos = list("DBAC")
    threes = [ch for ch in lines[3] if ch in string.ascii_letters]
    return list(zip(zeroes, ["A0", "B0", "C0", "D0"])) \
        + list(zip(ones, [a + '1' for a in "ABCD"])) \
        + list(zip(twos, [a + '2' for a in "ABCD"])) \
        + list(zip(threes, ["A3", "B3", "C3", "D3"]))


def travel_logic2(node, name, pm, room_cap="123"):  # return (is_legal, is_end)
    dst, nrg, path = node
    if dst in pm or dst in path:
        return False, False
    is_end = False
    prev = path[-1]
    if is_pos_in_doorway(prev) and is_pos_outer_room(dst):
        # entering a room
        if dst[0] != name[0]:
            return False, False  # wrong room, cannot enter
        # right room
        inner_rooms = [dst[0] + i for i in room_cap]
        inner_occs = [pm.get(inner_room) for inner_room in inner_rooms]
        any_wrong = any([io is not None and io[0] != dst[0] for io in inner_occs])
        if any_wrong:  # right room, but inner occupants are wrong, cannot enter the room
            return False, False
        elif len(inner_occs) > 0 and inner_occs[0] is None:
            return True, False  # good room, but fill in empty
        else:
            return True, True  # park
    elif is_pos_in_room(dst):
        is_entering = int(prev[-1]) < int(dst[-1])
        if prev[0] != name[0]:  # not match, allowed to only leave
            if is_entering:
                return False, False  # wrong room
            return True, False # leaving okay
        if is_entering:
            dst_idx = room_cap.index(dst[1])
            below_pos = [dst[0] + i for i in room_cap[dst_idx + 1:]]
            belows = [pm.get(bp) for bp in below_pos]
            if len(belows) == 0:
                return True, True
            if any([b is not None and (b[0] != dst[0]) for b in belows]):
                return False, False  # cannot block unmatched
            if any([b is None for b in belows]):
                return True, False  # good, but don't stop, keep entering
            else:
                return True, True  # can end!
        else:
            # exiting
            prev_idx = room_cap.index(prev[1])
            below_pos = [dst[0] + i for i in room_cap[prev_idx:]]
            belows = [pm.get(bp) for bp in below_pos]
            if any([b is None or b[0] != dst[0] for b in belows]):
                return True, False  # room has wrong elements, leave
            else:
                return False, False  # room is fully matched, don't leave

    src = path[0]
    # can settle in hallway (but not doorway) if started from room
    if is_pos_in_room(src) and is_pos_in_hall(dst) and not is_pos_in_doorway(dst):
        is_end = True
    return True, is_end


if __name__ == '__main__':
    main()
