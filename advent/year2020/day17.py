from advent import elf

"""
I had a suspicion that part 2 would add another dimension.
I'm sure there's a more elegant way to handle this, but I guess that's the "fun" of Conway's game of life
The two-pass approach isn't optimal, but it's fast enough and always works on the first attempt.
For Advent: I'd rather save myself minutes of debugging vs milliseconds of execution.
Same thing with how I "expanded" the cubes: not optimal, but it's best to code up what'll work and trim it down
or rework if it's not fast enough.
If it's fast enough, I can submit and move on.
"""


def is_active(char):
    return char == '#' or char == '&'


def safe_get(cube, layer, row, col):
    if 0 <= layer < len(cube):
        clayer = cube[layer]
        if 0 <= row < len(clayer):
            crow = clayer[row]
            if 0 <= col < len(crow):
                return crow[col]
    return '.'


def hc_safe_get(hcube, cube, layer, row, col):
    if 0 <= cube < len(hcube):
        return safe_get(hcube[cube], layer, row, col)
    return '.'


def safe_is_active(cube, layer, row, col):
    return is_active(safe_get(cube, layer, row, col))


def hc_safe_is_active(hcube, cube, layer, row, col):
    return is_active(hc_safe_get(hcube, cube, layer, row, col))


def count_active_around(cube, layer, row, col, skip_self=True):
    total = 0
    around = [-1, 0, 1]
    for ld in around:
        for rd in around:
            for cd in around:
                if skip_self and (ld == 0 and rd == 0 and cd == 0):
                    continue
                if safe_is_active(cube, layer + ld, row + rd, col + cd):
                    total += 1
    return total


def hc_count_active_around(hcube, cube, layer, row, col):
    total = 0
    for hd in [-1, 0, 1]:
        skip_self = (hd == 0)
        hh = cube + hd
        if not 0 <= hh < len(hcube):
            continue
        total += count_active_around(hcube[hh], layer, row, col, skip_self)
    return total


def create_cube(layers, rows, cols):
    cube = []
    for _ in range(layers):
        grid = []
        for _ in range(rows):
            grid.append(['.' for _ in range(cols)])
        cube.append(grid)
    return cube


def create_hypercube(cubes, layers, rows, cols):
    hypercube = []
    for _ in range(cubes):
        hypercube.append(create_cube(layers, rows, cols))
    return hypercube


def expand_cube(cube):
    new_cube = create_cube(len(cube) + 2, len(cube[0]) + 2, len(cube[0][0]) + 2)
    # inscribe
    for l, layer in enumerate(cube):
        for r, row in enumerate(layer):
            for c, col in enumerate(row):
                new_cube[l + 1][r + 1][c + 1] = col
    return new_cube


def expand_hypercube(hcube):
    new_hypercube = []
    cube = hcube[0]
    new_hypercube.append(create_cube(len(cube) + 2, len(cube[0]) + 2, len(cube[0][0]) + 2))
    for i, cube in enumerate(hcube):
        new_hypercube.append(expand_cube(cube))
    cube = hcube[0]
    new_hypercube.append(create_cube(len(cube) + 2, len(cube[0]) + 2, len(cube[0][0]) + 2))
    return new_hypercube


def cycle_cube(cube):
    # # is active    & was active, become inactive
    # . is inactive  ! was inactive, becomes active
    #
    for l, layer in enumerate(cube[:]):
        for r, row in enumerate(layer[:]):
            for c, col in enumerate(row[:]):
                active_around = count_active_around(cube, l, r, c)
                if is_active(col) and not (2 <= active_around <= 3):
                    cube[l][r][c] = '&'
                elif not is_active(col) and active_around == 3:
                    cube[l][r][c] = '!'
    for l, layer in enumerate(cube[:]):
        for r, row in enumerate(layer[:]):
            for c, col in enumerate(row[:]):
                if col == '&':
                    cube[l][r][c] = '.'
                elif col == '!':
                    cube[l][r][c] = '#'
    return cube


def cycle_hypercube(hcube):
    # # is active    & was active, become inactive
    # . is inactive  ! was inactive, becomes active
    for h, cube in enumerate(hcube[:]):
        for l, layer in enumerate(cube[:]):
            for r, row in enumerate(layer[:]):
                for c, col in enumerate(row[:]):
                    active_around = hc_count_active_around(hcube, h, l, r, c)
                    if is_active(col) and not (2 <= active_around <= 3):
                        hcube[h][l][r][c] = '&'
                    elif not is_active(col) and active_around == 3:
                        hcube[h][l][r][c] = '!'
    for h, cube in enumerate(hcube[:]):
        for l, layer in enumerate(cube[:]):
            for r, row in enumerate(layer[:]):
                for c, col in enumerate(row[:]):
                    if col == '&':
                        hcube[h][l][r][c] = '.'
                    elif col == '!':
                        hcube[h][l][r][c] = '#'
    return hcube


def print_cube(cube):
    for l, layer in enumerate(cube):
        print(f"Layer {l} / {len(cube)}")
        for r, row in enumerate(layer):
            print(''.join(row))


def count_active(cube):
    total = 0
    for layer in cube:
        for row in layer:
            for col in row:
                if is_active(col):
                    total += 1
    return total


def hc_count_active(hcube):
    return sum([count_active(cube) for cube in hcube])


def parse_lines_to_cube(lines):
    cube = create_cube(1, len(lines), len(lines[0]))
    for l, line in enumerate(lines):
        for c, char in enumerate(list(line)):
            cube[0][l][c] = char
    return cube


def part1(lines):
    cube = parse_lines_to_cube(lines)
    for i in range(6):
        cube = expand_cube(cube)
        cube = cycle_cube(cube)
        # print(f"After {i+1} cycles: {count_active(cube)} active")
    return count_active(cube)


def part2(lines):
    hcube = [parse_lines_to_cube(lines)]
    # print(f"After 0 cycles: {hc_count_active(hcube)} active")
    for i in range(6):
        hcube = expand_hypercube(hcube)
        hcube = cycle_hypercube(hcube)
        # print(f"After {i + 1} cycles: {hc_count_active(hcube)} active")
    return hc_count_active(hcube)


def main():
    lines = elf.read_lines(__file__)
    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
