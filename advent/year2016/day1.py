"""
TIL:
sys.stdin.readline().rstrip() for quick input
enums in Python are a little clunky
"""
from enum import IntEnum


def main():
    line = open("day1.txt").readline()
    print(part1(line))
    print(part2(line))


def part1(line):
    dirs = line.split(", ")
    x, y = 0, 0
    facing = Direction.North
    for d in dirs:
        if d.startswith("R"):
            facing = facing.turnRight()
        else:
            facing = facing.turnLeft()
        x, y = move(x, y, facing, int(d[1:]))
    return abs(x) + abs(y)


def move(x, y, facing, dist):
    if facing == Direction.North:
        return x, y + dist
    elif facing == Direction.East:
        return x + dist, y
    elif facing == Direction.South:
        return x, y - dist
    else:
        return x - dist, y


def part2(line):
    dirs = line.split(", ")
    x, y = 0, 0
    facing = Direction.North
    seen = set()
    for d in dirs:
        if d.startswith("R"):
            facing = facing.turnRight()
        else:
            facing = facing.turnLeft()
        x, y, location = moveAndTrack(x, y, facing, int(d[1:]), seen)
        if location is not None:
            lx, ly = location
            return abs(lx) + abs(ly)
    return None


def moveAndTrack(x, y, facing, dist, seen):
    newX, newY = x, y
    loc = None
    if facing == Direction.North:
        newY += dist
        for i in range(y + 1, newY + 1):
            step = (x, i)
            if loc is None and step in seen:
                loc = step
            seen.add(step)
    elif facing == Direction.East:
        newX += dist
        for i in range(x + 1, newX + 1):
            step = (i, y)
            if loc is None and step in seen:
                loc = step
            seen.add(step)
    elif facing == Direction.South:
        newY -= dist
        for i in range(y - 1, newY - 1, -1):
            step = (x, i)
            if loc is None and step in seen:
                loc = step
            seen.add(step)
    else:
        newX -= dist
        for i in range(x - 1, newX - 1, -1):
            step = (i, y)
            if loc is None and step in seen:
                loc = step
            seen.add(step)
    return newX, newY, loc


class Direction(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3

    def turnLeft(self):
        if self == Direction.North:
            return Direction.West
        else:
            return Direction(self - 1)

    def turnRight(self):
        if self == Direction.West:
            return Direction.North
        else:
            return Direction(self + 1)


if __name__ == "__main__":
    main()
