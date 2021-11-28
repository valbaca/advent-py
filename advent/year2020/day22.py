from advent import elf
from collections import deque


def score_deck(deck):
    temp = deque()
    n = len(deck)
    score = 0
    for i in range(n):
        t = deck.pop()
        score += (i + 1) * t
        temp.appendleft(t)
    for i in range(n):
        t = temp.pop()
        deck.appendleft(t)
    return score


def score_winner(decks):
    deck = decks[0] if len(decks[0]) > 0 else decks[1]
    return score_deck(deck)


def play_round(decks):
    p1, p2 = decks
    c1 = p1.popleft()
    c2 = p2.popleft()

    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)


def game_winner(decks):
    if len(decks[0]) == 0:
        return 1
    elif len(decks[1]) == 0:
        return 0
    return None


def play(decks):
    while game_winner(decks) is None:
        play_round(decks)
    return score_winner(decks)


def parse_decks(line_groups):
    decks = [deque(), deque()]
    for player, player_decks in enumerate(line_groups):
        deck = decks[player]
        for card_line in player_decks[1:]:
            deck.append(int(card_line))
    return decks


def part1(line_groups):
    return play(parse_decks(line_groups))


def clone_deque(orig, length):
    new_dq = orig.copy()
    while len(new_dq) > length:
        new_dq.pop()
    return new_dq


def play_recur_round(decks, layer, seen):
    scores = score_deck(decks[0]), score_deck(decks[1])
    if scores in seen:
        return 0, scores[0]
    else:
        seen.add(scores)
    p1, p2 = decks
    c1 = p1.popleft()
    c2 = p2.popleft()

    if c1 <= len(p1) and c2 <= len(p2):
        sub_game_winner, _ = play_recursively([clone_deque(p1, c1), clone_deque(p2, c2)], layer + 1)
        p1wins = sub_game_winner == 0
    else:
        p1wins = c1 > c2

    if p1wins:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)


def play_recursively(decks, layer=1):
    seen = set()
    while game_winner(decks) is None:
        winner = play_recur_round(decks, layer, seen)
        if winner is not None:
            return winner
    return game_winner(decks), score_winner(decks)


def part2(line_groups):
    return play_recursively(parse_decks(line_groups))


def main():
    line_groups = elf.lines_blank_grouped(elf.in_file(__file__))
    print(part1(line_groups))
    print(part2(line_groups))


if __name__ == '__main__':
    main()
