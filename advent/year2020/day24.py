from advent import elf

"""
Yet another Game of Life problem...
The twist here is instead of a finite box-grid, we have an infinite hex layout.

The same approach is valid:
- Relative grid by using a dict, tiles[x][y]
  - Always use this when the directions are "relative", don't bother with lists
- Two-pass Game of Life
  - One of these days I'll lookup a better way
I even went with a very sub-optimal way to handle the "borders":
- any black tile throws in all it's adjacent tiles into a set that's scanned later
"""


def get_dirs(line):
    dirs = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == 'w' or c == 'e':
            dirs.append(c)
            i += 1
        else:
            dirs.append(line[i:i + 2])
            i += 2
    return dirs


MOVE_DIFF = {'e': (1, 0),
             'se': (1, 1),
             'sw': (0, 1),
             'w': (-1, 0),
             'nw': (-1, -1),
             'ne': (0, -1)}

AROUND = sorted(MOVE_DIFF.values())


def follow_dirs(dirs):
    x, y = 0, 0
    # e, se, sw, w, nw, ne
    for d in dirs:
        xd, yd = MOVE_DIFF[d]
        x, y = x + xd, y + yd
    return x, y


def safe_tile_ctor(tiles, x, y):
    if x not in tiles:
        tiles[x] = {}
    if y not in tiles[x]:
        tiles[x][y] = {'w?': True}
    return tiles[x][y]


def flip_tile(tile):
    tile['w?'] = not tile['w?']


def count_all_black_tiles(tiles):
    total = 0
    for x in tiles:
        for y in tiles[x]:
            if is_black(tiles, x, y):
                total += 1
    return total


def part1(lines):
    tiles = {}
    for line in lines:
        dirs = get_dirs(line)
        x, y = follow_dirs(dirs)
        flip_tile(safe_tile_ctor(tiles, x, y))
    return count_all_black_tiles(tiles), tiles


def is_black(tiles, x, y):
    if x not in tiles or y not in tiles[x]:
        return False
    else:
        return not tiles[x][y]['w?']


def coords_around(x, y):
    return [(x + xd, y + yd) for xd, yd in AROUND]


def count_black_around(tiles, x, y):
    total = 0
    for xx, yy in coords_around(x, y):
        if is_black(tiles, xx, yy):
            total += 1
    return total


def one_day(tiles):
    border_tiles = set()
    for x in tiles:
        for y in tiles[x]:
            tile = tiles[x][y]
            black_around = count_black_around(tiles, x, y)
            is_b = is_black(tiles, x, y)
            if is_b and (black_around == 0 or black_around > 2):
                # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                tile['next?'] = True  # White
            elif (not is_b) and (black_around == 2):
                # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                tile['next?'] = False  # Black
            if is_b:
                # Optimize?
                border_tiles.update(coords_around(x, y))
    for x, y in list(border_tiles):
        if is_black(tiles, x, y):
            continue
        if count_black_around(tiles, x, y) == 2:
            tile = safe_tile_ctor(tiles, x, y)
            tile['next?'] = False  # Black
    for x in tiles:
        for y in tiles[x]:
            tile = tiles[x][y]
            if 'next?' in tile:
                tile['w?'] = tile['next?']
                del tile['next?']
    return count_all_black_tiles(tiles), tiles

    # (These were my "to do" notes, leaving them in to show how I approached:
    # write an 'around' function to get how many black tiles around a given x, y
    # probably easiest to still do a two-pass algorithm
    # write something like tile['next_w?']: True (turning white) False (turning black) None (no change)
    # Don't forget to check the "bounds" for tiles that were untouched and newly flip to black


def part2(tiles, days):
    print(f"Day 0: {count_all_black_tiles(tiles)}")
    for day in range(1, days + 1):
        c, tiles = one_day(tiles)
        print(f"Day {day}: {c}")
    return c


def main():
    lines = elf.read_lines(__file__)
    ans1, tiles = part1(lines)
    print(ans1)
    print(part2(tiles, 100))


if __name__ == '__main__':
    main()
