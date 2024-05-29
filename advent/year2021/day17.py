from advent import elf

"""
TIL: I thought the hard part would be solving the problem, but it was actually
just making sure I read the instructions properly and off-by-one errors.
"""


def main():
    lines = elf.read_lines(__file__)
    print(together(lines))


xlo, xhi, ylo, yhi = 0, 0, 0, 0


def together(lines):
    global xlo, xhi, ylo, yhi
    xlo, xhi, ylo, yhi = elf.only_ints(elf.septoi(lines[0], r"[^0-9-]"))
    mx = -1
    count = 0
    scale = 2
    for x in range(-abs(xhi) * scale, abs(xhi) * scale):
        for y in range(-abs(yhi) * scale, abs(yhi) * scale):
            hits, peak = is_hit(x, y)
            if hits:
                count += 1
                if peak > mx:
                    mx = peak
    return mx, count


def is_hit(ixv, iyv):
    # ixv = initial x velocity, ixy = initial y velocity
    x, y, xv, yv = 0, 0, ixv, iyv
    max_y = 0
    # originally had a bug here, was using > instead of >=
    while y >= ylo:
        if max_y < y:
            max_y = y
        x += xv
        y += yv
        # also had a bug here: initialy wasn't handling xv == 0 correctly
        if xv > 0:
            xv -= 1
        elif xv < 0:
            xv += 1
        yv -= 1
        if within(x, y):
            return True, max_y
    return False, -1


def within(x, y):
    return (xlo <= x <= xhi) and (ylo <= y <= yhi)


if __name__ == '__main__':
    main()
