import itertools
import math

import networkx as nx

from advent import elf

# Now this one was fun. Really got to flex with numpy and networkx here.

def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


def maze_to_graph_and_locations(maze):
    h, w = maze.shape
    g = nx.Graph()
    locs = {}  # name of the location '0' to position (2,3)

    for r in range(h):
        for c in range(w):
            if (ch := maze[r, c]) != '#':  # skip walls
                if ch != '.':
                    locs[ch] = (r, c)
                g.add_node((r, c))
                arounds = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for r2, c2 in arounds:  # add edges to accessible, non-wall locations
                    if 0 <= r2 < h and 0 <= c2 < w:
                        if maze[r2, c2] != '#':
                            g.add_edge((r, c), (r2, c2))
    return g, locs


def part1(lines, origin_return=False):
    # This is basically a two-layer traveling salesman:
    # parse the input (simply split? into numpy? boolean wall=False, path=True), or convert into full node graph?
    # for each input, find the dist to each other point (A*/TSP)
    maze = elf.lines_to_np_array(lines)
    maze_graph, locs = maze_to_graph_and_locations(maze)
    dists = {}  # ('0','1'): dist-from-0-to-1
    # use the maze graph to build the "point-to-point distance" map
    for name, pos in locs.items():
        for other_name, other_pos in locs.items():
            dist = nx.shortest_paths.shortest_path_length(maze_graph, source=pos, target=other_pos)
            dists[(name, other_name)] = dist
            dists[(other_name, name)] = dist

    # This part is manual (not using networkx) b/c it doesn't seem to support this exact use-case of
    # finding the shortest hamiltonian PATH with a specified START node
    # Note, part2 *DOES* return back, so I could've used traveling_salesman_problem but it was easier to just reuse
    to_visit = sorted(name for name in locs.keys() if name != '0')
    ans = math.inf
    for rest_path_perm in itertools.permutations(to_visit):
        path = ['0'] + list(rest_path_perm)
        if origin_return:
            path += ['0']
        ans = min(ans, sum(dists[ab] for ab in itertools.pairwise(path)))
        # print(ans)
    return ans


def part2(lines):
    return part1(lines, origin_return=True)


if __name__ == '__main__':
    main()
