from advent import elf


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


def follow_dirs(dirs):
    x, y = 0, 0
    # e, se, sw, w, nw, ne
    for d in dirs:
        xd, yd = MOVE_DIFF[d]
        x, y = x + xd, y + yd
    return x, y


def safe_get_title(tiles, x, y):
    if x not in tiles:
        tiles[x] = {}
    if y not in tiles[x]:
        tiles[x][y] = {'w?': True}
    return tiles[x][y]


def flip_tile(tile):
    tile['w?'] = not tile['w?']


def part1(lines):
    tiles = {}
    for line in lines:
        dirs = get_dirs(line)
        x, y = follow_dirs(dirs)
        flip_tile(safe_get_title(tiles, x, y))
    total = 0
    for xt in tiles:
        for yt in tiles[xt]:
            if not tiles[xt][yt]['w?']:
                total += 1
    return total


def part2(lines):
    pass
    # code here


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
