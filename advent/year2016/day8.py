import numpy as np

from advent import elf


def main():
    test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1(test_lines, wide=7, tall=3))

    lines = elf.read_lines(__file__)
    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


class Screen:
    def __init__(self, tall, wide):
        self.screen = np.zeros((tall, wide))

    def turn_on(self, wide, tall):
        self.screen[:tall, :wide] = 1

    def rotate_row(self, row_a, right_b_pixels):
        # we "roll"/rotate the whole screen, but then pluck out the row
        rotated_row = np.roll(np.copy(self.screen), right_b_pixels, axis=1)[row_a, :]
        self.screen[row_a, :] = rotated_row

    def rotate_col(self, col_a, down_b_pixels):
        # we "roll"/rotate the whole screen, but then pluck out the col
        rotated_column = np.roll(np.copy(self.screen), down_b_pixels, axis=0)[:, col_a]
        self.screen[:, col_a] = rotated_column

    def parse_line(self, line):
        words = line.split(" ")
        if line.startswith('rect'):
            a, b = words[-1].split('x')
            self.turn_on(wide=int(a), tall=int(b))
        elif line.startswith('rotate column'):
            col_a = int(words[2].removeprefix("x="))
            down_b_pixels = int(words[4])
            self.rotate_col(col_a, down_b_pixels)
        elif line.startswith('rotate row'):
            row_a = int(words[2].removeprefix("y="))
            right_b_pixels = int(words[4])
            self.rotate_row(row_a, right_b_pixels)

    def print_screen(self):
        for row in self.screen:
            print(''.join('#' if pixel == 1 else '.' for pixel in row))
        print()


def part1(lines, wide=50, tall=6):
    s = Screen(wide=wide, tall=tall)
    # s.print_screen()
    for line in lines[:]:
        # print(line.strip())
        s.parse_line(line)
        # s.print_screen()
    return int(s.screen.sum())


def part2(lines, wide=50, tall=6):
    s = Screen(wide=wide, tall=tall)
    # s.print_screen()
    for line in lines[:]:
        # print(line.strip())
        s.parse_line(line)
        # s.print_screen()
    s.print_screen()
    return ""


if __name__ == '__main__':
    main()
