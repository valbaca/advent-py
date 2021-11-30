import math
import re

from advent import elf

"""
Here be...sea monsters
I really, really did not like this one...but I'm glad I stuck with it and finished.
I'm more glad that I'm doing this in Python instead of literally any other language because this would've been a nightmare.

I guess I really should've solved part 1 "correctly" by actually rearranging the tiles (rotating and flipping).
But that's the advantage of lazy coding vs eager: if you need it, you'll have to code it anyway.

Problems like this do "reward" me for poor coding. Just cobbling it together gets the solution b/c Python's fast enough.
"""


def main():
    lines = elf.lines_blank_grouped(elf.in_file(__file__))
    print(part1(lines))
    print(part2(lines))


def get_left_edge(image):
    edge = []
    for row in image:
        edge.append(row[0])
    return ''.join(edge)


def get_right_edge(image):
    edge = []
    for row in image:
        edge.append(row[-1])
    return ''.join(edge)


def get_top_edge(image):
    return image[0]


def get_bottom_edge(image):
    return image[-1]


def get_edges(image):
    return [
        (get_left_edge(image), 'left'),
        (get_right_edge(image), 'right'),
        (get_top_edge(image), 'top'),
        (get_bottom_edge(image), 'bottom')]


def match_tile_pair(a, b):
    a_id, b_id = a['id'], b['id']
    if a_id == b_id:
        return
    aedges = get_edges(a['image'])
    bedges = get_edges(b['image'])
    for a_edge, a_side in aedges:
        for b_edge, b_side in bedges:
            if a_edge == b_edge or a_edge == b_edge[::-1]:
                a['edges'].add(b_id)
                b['edges'].add(a_id)
                if a_edge == b_edge:
                    a['sides'][a_side] = b_id, b_side
                    b['sides'][b_side] = a_id, a_side
                else:
                    a['sides'][a_side] = b_id, "!" + b_side
                    b['sides'][b_side] = a_id, "!" + a_side


def match_all_tiles(tiles):
    for a in tiles:
        for b in tiles:
            match_tile_pair(a, b)
    return tiles


def parse_tile(lines):
    tile_id = int(re.split(r"[\s:]", lines[0])[1])
    image = lines[1:]
    return {'id': tile_id, 'image': image, 'edges': set(), 'sides': {}}


def part1(line_groups):
    tiles = [parse_tile(line_group) for line_group in line_groups]
    tiles = match_all_tiles(tiles)
    corner_tiles = [t['id'] for t in tiles if len(t['edges']) == 2]
    return elf.product(corner_tiles)


def print_image(image):
    for row in image:
        print(''.join(row))


def rotate(image):
    rotated = [row[:] for row in image]
    for r in range(len(image)):
        rotated[r] = ''.join(reversed([image[i][r] for i in range(len(image))]))
    return rotated


def flip(image):
    return [''.join(reversed(row)) for row in image]


def all_arrangements(image):
    arr = [image]
    for _ in range(3):
        arr.append(rotate(arr[-1]))
    arr.append(flip(image))
    for _ in range(3):
        arr.append(rotate(arr[-1]))
    return arr


def get_tile_by_id(tiles, id):
    return [t for t in tiles if t['id'] == id][0]


def fits(grid, image, r, c):
    if r == 0 and c == 0:
        return True
    if r == 0:
        return get_right_edge(grid[r][c - 1]) == get_left_edge(image)
    elif c == 0:
        return get_bottom_edge(grid[r - 1][c]) == get_top_edge(image)
    else:
        return get_right_edge(grid[r][c - 1]) == get_left_edge(image) and get_bottom_edge(
            grid[r - 1][c]) == get_top_edge(image)


def build_options(tiles, grid, grid_ids, next_n):
    r = next_n // len(grid)
    c = next_n % len(grid)
    if c == 0:
        near_tile = get_tile_by_id(tiles, grid_ids[r - 1][c])  # up
    else:
        near_tile = get_tile_by_id(tiles, grid_ids[r][c - 1])  # left
    all_edge_ids = near_tile['edges']
    seen = [i for row in grid for i in row]
    return [get_tile_by_id(tiles, e) for e in all_edge_ids if e not in seen]


def normalize_sub(tiles, grid, grid_ids, try_tile, n):
    # print(f"n = {n} Trying {try_tile}")
    r = n // len(grid)
    c = n % len(grid)
    for a in all_arrangements(try_tile['image']):
        # check fit: left and up; if invalid, continue to next arrangement
        if not fits(grid, a, r, c):
            continue
        # if fits, place tile
        grid[r][c] = a
        grid_ids[r][c] = try_tile['id']
        # if solved, return
        if r == len(grid) - 1 and c == len(grid) - 1:
            return grid  # Solution!
        # if valid but unsolved, recur to next slots
        options = build_options(tiles, grid, grid_ids, n + 1)
        for option in options:
            out = normalize_sub(tiles, grid, grid_ids, option, n + 1)
            if out is not None:
                return out
    grid[r][c] = None


def normalize(tiles):
    n = int(math.sqrt(len(tiles)))
    grid = [[None for _ in range(n)] for _ in range(n)]
    grid_ids = [[None for _ in range(n)] for _ in range(n)]
    corner_tiles = [t for t in tiles if len(t['edges']) == 2]
    for corner in corner_tiles:
        out = normalize_sub(tiles, grid, grid_ids, corner, 0)
        if out is not None:
            return out
    return None


def print_tiles(tiles):
    for grid_row in tiles:
        sample = grid_row[0]
        for r in range(len(sample)):
            for image in grid_row:
                print(image[r], end=' ')
            print()
        print()
    return


def merge_tiles(tiles):
    merged = []
    for gr, grid_row in enumerate(tiles):
        sample = grid_row[0]
        for r in range(1, len(sample) - 1):
            merged.append(''.join([image[r][1:-1] for image in grid_row]))
    return merged


def print_image(image):
    for row in image:
        print(row)


def find_sea_monster_at(image, r, c):
    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]
    if len(image) < r + len(monster) - 1 or len(image[r]) < c + len(monster[0]) - 1:
        return False
    for mr, monster_row in enumerate(monster):
        for mc, mchar in enumerate(monster_row):
            if mchar == '#' and image[r + mr][c + mc] != '#':
                return False
    return True


def find_sea_monsters(image):
    total = 0
    for r in range(len(image)):
        for c in range(len(image[r])):
            monster_at = find_sea_monster_at(image, r, c)
            if monster_at:
                total += 1
    if total > 0:
        return total


def count_hashes(image):
    return sum([1 if c == '#' else 0 for row in image for c in row])


def find_any_sea_monsters(image):
    for a in all_arrangements(image):
        monsters = find_sea_monsters(a)
        if monsters is not None:
            # print(f"Found {monsters} sea monsters")
            roughness = count_hashes(image) - (15 * monsters)
            # print(f"Roughness {roughness}")
            return roughness


def part2(line_groups):
    tiles = [parse_tile(line_group) for line_group in line_groups]
    tiles = match_all_tiles(tiles)
    tiles = normalize(tiles)
    # print_tiles(tiles)
    full_image = merge_tiles(tiles)
    # print_image(full_image)
    return find_any_sea_monsters(full_image)


if __name__ == '__main__':
    main()
