def main():
    with open("day2.txt") as fin:
        kp_out = ""
        kp = Keypad()
        akp_out = ""
        akp = AdvancedKeypad()
        for line in fin:
            line = line.rstrip()
            for ch in line:
                kp.move(ch)
                akp.move(ch)
            kp_out += str(kp.pos)
            akp_out += akp.get_pos()
        print(kp_out)  # part 1
        print(akp_out)  # part 2


class Keypad:
    """
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(self):
        self.pos = 5

    def move(self, pos):
        if pos == 'U':
            self._up()
        elif pos == 'D':
            self._down()
        elif pos == 'R':
            self._right()
        elif pos == 'L':
            self._left()

    def _up(self):
        if self.pos > 3:
            self.pos -= 3

    def _down(self):
        if self.pos < 7:
            self.pos += 3

    def _right(self):
        if self.pos % 3 != 0:
            self.pos += 1

    def _left(self):
        if self.pos % 3 != 1:
            self.pos -= 1


# not great, but works
keypad = "  1   234 56789 ABC   D  "


class AdvancedKeypad():
    def __init__(self):
        self.index = 10

    def get_pos(self):
        return keypad[self.index]

    def move(self, pos):
        if pos == 'U':
            self._up()
        elif pos == 'D':
            self._down()
        elif pos == 'R':
            self._right()
        elif pos == 'L':
            self._left()

    def _up(self):
        if self.index - 5 >= 0 and keypad[self.index - 5] != ' ':
            self.index -= 5

    def _down(self):
        if self.index + 5 < len(keypad) and keypad[self.index + 5] != ' ':
            self.index += 5

    def _right(self):
        if self.index % 5 != 4 and keypad[self.index + 1] != ' ':
            self.index += 1

    def _left(self):
        if self.index % 5 != 0 and keypad[self.index - 1] != ' ':
            self.index -= 1


if __name__ == "__main__":
    main()
