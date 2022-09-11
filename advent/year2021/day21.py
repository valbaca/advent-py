from collections import defaultdict
from itertools import product
from advent import elf

"""
TIL: This reminds me of another problem with similar branching.
Part 2 still ran very slow, but did complete. 

Ran nearly 10x faster with pypy! (but as of Sep 2022, still limited to 3.9)

pypy advent/year2021/day21.py  23.68s user 0.20s system 99% cpu 23.926 total
versus
python advent/year2021/day21.py  285.70s user 0.71s system 99% cpu 4:46.64 total

Installing pypy with pyenv:
pyenv versions | grep pypy # get the latest version. Latest is only 3.9
pyenv install pypy3.9-7.3.9 # globally install current latest pypy
pyenv local 3.10.5 pypy3.9-7.3.9 # make both python and pypy available locally
"""

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


def part1(lines):
    game = Game(parse_starts(lines), DeterministicDie())
    return game.play()

def parse_starts(lines):
    return [elf.septoi(line)[-1] for line in lines]

def omod(val, *, min=1, incl_max):
    """
    Performs offset modulus. (max is inclusive).
    Keep numbers as most people expect, as in "one to ten" == [1,10]
    """
    return ((val-min)%(incl_max+1-min))+min

class Game:
    def __init__(self, starts, die):
        self.pos = starts
        self.scores = [0 for _ in range(len(starts))]
        self.player = 0
        self.die = die
        self.rolls = 0
        self.size = 10
        self.winning = 1000
        self.rolls_per_turn = 3
    
    def play(self):
        while True:
            sum_roll = 0
            for _ in range(self.rolls_per_turn):
                sum_roll += next(self.die)
            self.rolls += self.rolls_per_turn
            self.pos[self.player] = omod(self.pos[self.player] + sum_roll, incl_max=10)
            self.scores[self.player] += self.pos[self.player]
            if self.scores[self.player] >= self.winning:
                return self.scores[(self.player+1) % len(self.scores)] * self.rolls
            self.player = (self.player+1) % len(self.scores) # next player
    
    def has_winner(self):
        return any(score >= self.winning for score in self.scores)

class DeterministicDie:
    def __init__(self, sides=100, start=1):
        self.sides = sides
        self.side = start-1

    def __next__(self):
        self.side += 1
        if self.side > self.sides:
            self.side = 1
        return self.side

###########################################################




def part2(lines):
    roll_spread = defaultdict(int)
    for roll in product([1,2,3], repeat=3):
        roll_spread[sum(roll)] += 1 # roll value to # of universes
    # print(roll_spread)
    QGame.roll_spread = roll_spread.items()
    qgame = QGame(parse_starts(lines), [0,0], False)
    return qgame.play()
    # Gives [716241959649754, 436714381695627] which I just ran max on afterward

class QGame:
    roll_spread = {}
    board_size = 10
    winning_score = 21

    def __init__(self, pos, scores, player):
        self.pos = pos # positions [player0, player1]
        self.scores = scores
        self.player = player # False = Player 1; True = Player 2
    
    def play(self):
        # switching to recursive
        if self.scores[not self.player] >= QGame.winning_score:
            return [1 if score >= QGame.winning_score else 0 for score in self.scores]
        # print(self.scores)
        wins = [0, 0]
        # next_player = not self.player
        for roll_value, universes in QGame.roll_spread:
            sub_pos = self.pos[:]
            sub_pos[self.player] = omod(sub_pos[self.player] + roll_value, incl_max=10)
            sub_scores = self.scores[:]
            sub_scores[self.player] += sub_pos[self.player]    
            sub_game = QGame(sub_pos, sub_scores, not self.player)
            sub_game_results = sub_game.play()
            for iplayer, player_wins in enumerate(sub_game_results):
                wins[iplayer] += (player_wins * universes)
        return wins
    
    def has_winner(self):
        return any(score >= self.winning for score in self.scores)

if __name__ == '__main__':
    main()
