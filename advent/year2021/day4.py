from advent import elf


def main():
    test_lines = elf.lines_blank_grouped(elf.test_file(__file__))
    lines = elf.lines_blank_grouped(elf.in_file(__file__))
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    to_call = list(map(int, lines[0][0].split(",")))
    boards = list(map(parse_board, lines[1:]))
    called = set()
    for call in to_call:
        called.add(call)
        for board in boards:
            if has_win(called, board):
                print("BINGO!")
                return score(call, called, board)


def parse_board(board_list):
    return [elf.int_list(row.split(" ")) for row in board_list]


def has_win(called: set, board):
    for row in board:
        set_row = set(row)
        if called.issuperset(set_row):
            return True
    for i in range(len(board[0])):
        set_col = set([row[i] for row in board])
        if called.issuperset(set_col):
            return True
    return False


def score(last_call, called, board):
    unmarked = [n for row in board for n in row if n not in called]
    total = sum(unmarked)
    return total * last_call


def part2(lines):
    to_call = list(map(int, lines[0][0].split(",")))
    boards = list(map(parse_board, lines[1:]))
    called = set()
    solved_boards = set()
    board_scores = [None] * len(boards)
    for call in to_call:
        called.add(call)
        for board_num, board in enumerate(boards):
            if board_num not in solved_boards and has_win(called, board):
                solved_boards.add(board_num)
                board_scores[board_num] = score(call, called, board)
                if len(solved_boards) == len(boards):
                    return board_scores[board_num]


if __name__ == '__main__':
    main()
