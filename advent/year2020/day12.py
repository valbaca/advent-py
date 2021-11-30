from advent import elf


def main():
    lines = elf.read_lines(__file__, parse)
    print(part1(lines))
    print(part2(lines))


def parse(line):
    return line[0], int(line[1:])


def move_boat(boat, move, dist):
    if move == 'N':
        boat['north'] += dist
    elif move == 'S':
        boat['north'] -= dist
    elif move == 'E':
        boat['east'] += dist
    elif move == 'W':
        boat['east'] -= dist
    return boat


DIRS = ['N', 'E', 'S', 'W']


def move_left(boat):
    idx = DIRS.index(boat['dir'])
    boat['dir'] = DIRS[idx - 1]


def move_right(boat):
    idx = DIRS.index(boat['dir'])
    boat['dir'] = DIRS[(idx + 1) % len(DIRS)]


def part1(lines):
    boat = {'dir': 'E', 'east': 0, 'north': 0}
    for move, dist in lines:
        if move == 'L':
            while dist > 0:
                move_left(boat)
                dist -= 90
        elif move == 'R':
            while dist > 0:
                move_right(boat)
                dist -= 90
        elif move == 'F':
            move_boat(boat, boat['dir'], dist)
        else:
            move_boat(boat, move, dist)
    return abs(boat['east']) + abs(boat['north'])


def rotate_waypoint_left(data):
    tmp = data['wayp']['east']
    data['wayp']['east'] = (-data['wayp']['north'])
    data['wayp']['north'] = tmp


def rotate_waypoint_right(data):
    for i in range(3):
        rotate_waypoint_left(data)


def part2(lines):
    data = {'boat': {'east': 0, 'north': 0},  # boat is absolute
            'wayp': {'east': 10, 'north': 1}}  # waypoint is relative
    for move, dist in lines:
        if move == 'L':
            while dist > 0:
                rotate_waypoint_left(data)
                dist -= 90
        elif move == 'R':
            while dist > 0:
                rotate_waypoint_right(data)
                dist -= 90
        elif move == 'F':
            for i in range(dist):
                data['boat']['east'] += data['wayp']['east']
                data['boat']['north'] += data['wayp']['north']
        else:
            move_boat(data['wayp'], move, dist)
    return abs(data['boat']['east']) + abs(data['boat']['north'])


if __name__ == '__main__':
    main()
