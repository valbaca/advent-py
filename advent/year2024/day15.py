from advent import elf
from advent.elf import ad, get


# Basically my approach is handle the moves in "waves" (curr and next)
# staring with the position of '@' get the next position in the direction.
# If it's a wall, then we hit a wall and nothing moves.
# If it's a box, then that's the next, and we continue.
# If it's an empty space, then we can stop checking and move everything up one position:
# @O. becomes @ ? O ? . ! => @@O
# Finally, we overwrite the previous position of '@' with .

# For part 2, it's a bit more involved but basically the same.
# Instead, we have multiple "current" and next positions to handle the boxes pushing multiple overlapping boxes
#  @     < start with '@' as the single current
#  []    < which adds BOTH of these
# [][]   < which will then add all four of these

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


def part1(lines):
    g = []
    for line in lines:
        if '#' in line:
            g.append(list(line))
        else:
            for ch in list(line):
                grid_move(g, ch)
                # print(f"Move {ch}")
                # for row in g:
                #     print(''.join(row))
    return gps_score(g)


DIRS = {
    '^': (-1, 0),
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1),
}


def grid_move(g, dir):
    orig = [(r, c) for r, row in enumerate(g) for c, ch in enumerate(row) if ch == '@'][0]
    cur_pos = orig
    cur = get(g, cur_pos)
    to_move = []
    while cur != '.' and cur != '#':
        to_move.append(cur_pos)
        cur_pos = ad(cur_pos, DIRS[dir])
        cur = get(g, cur_pos)
    if cur == '#':
        ...  # nothing moves
    elif cur == '.':
        while to_move:
            tail = to_move.pop()
            tgt = ad(tail, DIRS[dir])
            g[tgt[0]][tgt[1]] = g[tail[0]][tail[1]]
        g[orig[0]][orig[1]] = '.'  # leave '.' where @ originally was


def gps_score(g):
    return sum(
        rowi * 100 + coli
        for [rowi, _row, coli, col] in elf.enumerate_grid(g)
        if col == 'O'
    )


def part2(lines):
    g = []
    for line in lines:
        if '#' in line:
            row = []
            for ch in list(line):
                if ch == '#':
                    row.extend(['#', '#'])
                elif ch == 'O':
                    row.extend(['[', ']'])
                elif ch == '.':
                    row.extend(['.', '.'])
                elif ch == '@':
                    row.extend(['@', '.'])
            g.append(row)
        else:
            for ch in list(line):
                g = big_grid_move(g, ch)
                # print(f"Move {ch}")
                # for row in g:
                #     print(''.join(row))
    return big_gps_score(g)


def big_grid_move(g, dir):
    orig = [(r, c) for r, row in enumerate(g) for c, ch in enumerate(row) if ch == '@'][0]
    currents = [orig]
    to_move = []
    nothing_moves = False
    while currents:
        next_currents = []
        for cur in currents:
            cur_val = get(g, cur)
            if cur_val == '#':
                # hit a wall
                nothing_moves = True
                currents = []
                break
            if cur_val == '.': # This took way to long to realize! empty space doesn't push!
                continue
            to_move.append(cur)
            next = ad(cur, DIRS[dir])
            next_currents.append(next)
            # we only add the half of the box if we're moving up and down; left to right just uses the same logic
            if dir == '^' or dir == 'v':
                next_val = get(g, next)
                if next_val == '[':
                    right_half = ad(next, (0, 1))
                    assert get(g, right_half) == ']' # These asserts saved me!
                    if right_half not in next_currents:
                        next_currents.append(right_half)  # add right-half of box
                if next_val == ']':
                    left_half = ad(next, (0, -1))
                    assert get(g, left_half) == '['  # These asserts saved me!
                    if left_half not in next_currents:
                        next_currents.append(left_half)  # add right-half of box
        # check if all next_currents are empty, in which case we can actually complete the move!
        if all('.' == get(g, next_current) for next_current in next_currents):
            currents = []
        else:
            currents = next_currents
    if nothing_moves:
        return g
    else:
        new_grid = [row.copy() for row in g]
        for pos in to_move:
            new_grid[pos[0]][pos[1]] = '.'
        while to_move:
            tail = to_move.pop()
            tgt = ad(tail, DIRS[dir])
            new_grid[tgt[0]][tgt[1]] = g[tail[0]][tail[1]]
        return new_grid


def big_gps_score(g):
    return sum(
        rowi * 100 + coli
        for [rowi, _row, coli, col] in elf.enumerate_grid(g)
        if col == '['
    )


if __name__ == '__main__':
    main()

# 1354545 too low
