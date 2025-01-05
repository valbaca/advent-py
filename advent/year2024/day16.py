from advent import elf
from advent.elf import ad, get, clockwise, counterclockwise, E, DIRS, to_grid, mv

import heapq

# Solved part 2 with pure brute force and letting it run for several hours

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

def setup(lines):
    g = to_grid(lines)
    start = [(r, c) for [r,c, v] in elf.iter_grid(g) if v == 'S'][0]
    g[start[0]][start[1]] = '.'
    end =  [(r, c) for [r,c, v] in elf.iter_grid(g) if v == 'E'][0]
    g[end[0]][end[1]] = '.'
    return g, start, end


def part1(lines):
    g, start, end = setup(lines)
    return Astar(g, (start, E)).a_star_directional(end)


class Astar:
    def __init__(self, g, start):
        self.g = g
        self.start = start
        self.g_score = {self.start: 0}

    def heuristic(self, a, b):
        # Manhattan distance as the heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        pos, d = node
        return [
            (1 if d == nd else 1001, (new_pos, nd))
            for nd in DIRS
            if get(self.g, (new_pos := mv(pos, nd))) == '.'
        ]


    def a_star_directional(self, end, end_d=None, cutoff=None):
        if get(self.g, end) == '#':
            return None
        # heap is using (score, node)
        q = []
        heapq.heappush(q, (0, self.start))


        f_score = {self.start: self.heuristic(self.start[0], end)}

        low_score = self.g_score.get(end)  # type: int | None

        while q:
            curr_score, curr = heapq.heappop(q)
            if cutoff and cutoff < curr_score:
                # print("!")
                return low_score

            if curr[0] == end and (end_d is None or curr[1] == end_d):
                score = self.g_score[curr]
                if low_score is None or score < low_score:
                    low_score = score
                return low_score

            for move_cost, neighbor in self.neighbors(curr):
                new_score = self.g_score[curr] + move_cost
                if neighbor not in self.g_score or new_score <= self.g_score[neighbor]:
                    self.g_score[neighbor] = new_score
                    f_score[neighbor] = new_score + self.heuristic(neighbor[0], end)
                    heapq.heappush(q, (f_score[neighbor], neighbor))

        return low_score


def part2(lines):
    g, start, end = setup(lines)

    from_start = Astar(g, (start, E))

    # low_score = a_star_directional(g, (start, E), end)
    low_score = from_start.a_star_directional(end)
    # print(low_score)
    seats = set()
    for [r,c] in elf.iter_grid_indexes(g):
        if get(g, (r,c)) == '#':
            continue
        mid = (r,c)
        for d in DIRS:
            start_to_mid = from_start.a_star_directional(mid, end_d=d, cutoff=low_score)
            if start_to_mid is None or start_to_mid > low_score:
                continue
            from_mid = Astar(g, (mid, d))
            mid_to_end = from_mid.a_star_directional(end, cutoff=low_score-start_to_mid)
            if mid_to_end is not None and low_score == start_to_mid + mid_to_end:
                seats.add(mid)
                break
        # print(mid)
    return len(seats)


if __name__ == '__main__':
    main()
