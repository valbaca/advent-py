import logging
from collections import Counter
from functools import cached_property

from advent import elf
from advent.elf import cmp

# TIL: @cached_property and "offensive programming" helped here
# offensive programming is checking what "shouldn't happen" and throwing errors

logger = logging.Logger(__name__)
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
    hands = [Hand(line) for line in lines]
    sorted_hands = sorted(hands)
    return sum(
        (i+1) * h.score
        for i, h in enumerate(sorted_hands)
    )

cards = "23456789TJQKA"
card_vals = {c: int(i) for i, c in enumerate(list(cards))}

def cmp_card(a, b):
    return cmp(card_vals[a], card_vals[b])

class Hand:
    def __init__(self, line):
        splits = elf.septoi(line)
        self.hand = str(splits[0])
        self.score = int(splits[1])

    def __repr__(self):
        return f"{self.hand} {self.score}"


    @cached_property
    def hand_type(self):
        top = 7
        counted = Counter(list(self.hand))
        if len(counted) == 1:
            return top # Five of a Kind
        if len(counted) == 2:
            if 4 in counted.values():
                return top - 1 # Four of a Kind
            elif 3 in counted.values() and 2 in counted.values():
                return top - 2 # Full House
            else:
                raise NotImplementedError(f"hand_type error 2 {self.hand}")
        if len(counted) == 3:
            if 3 in counted.values():
                return top - 3 # Three of a Kind
            elif list(sorted(counted.values())) == [1,2,2]:
                return top - 4 # Two Pair
            else:
                raise NotImplementedError(f"hand_type error 3 {self.hand}")
        if len(counted) == 4:
            if list(sorted(counted.values())) == [1,1,1,2]:
                return top - 5 # One Pair
            else:
                raise NotImplementedError(f"hand_type error 4 {self.hand}")
        if len(counted) == 5:
            return top - 6
        raise NotImplementedError(f"hand_type error 5 {self.hand}")

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        return self.__cmp__(other) < 0
    def __cmp__(self, other):
        types_cmp = cmp(self.hand_type, other.hand_type)
        if types_cmp != 0:
            return types_cmp
        for sc, oc in zip(list(self.hand), list(other.hand)):
            compared_cards = cmp_card(sc, oc)
            if compared_cards != 0:
                return compared_cards
        logger.debug(f"Two cards considered equal: {self.hand} - {other.hand}")
        return 0


def part2(lines):
    hands = [Hand2(line) for line in lines]
    sorted_hands = sorted(hands)
    return sum(
        (i+1) * h.score
        for i, h in enumerate(sorted_hands)
    )

cards2 = "J23456789TQKA"
card_vals2 = {c: int(i) for i, c in enumerate(list(cards2))}

def cmp_card2(a, b):
    return cmp(card_vals2[a], card_vals2[b])

class Hand2:
    def __init__(self, line):
        splits = elf.septoi(line)
        self.hand = str(splits[0])
        self.score = int(splits[1])

    def __repr__(self):
        return f"{self.hand} {self.score}"


    @cached_property
    def hand_type(self):
        top = 7
        counted = Counter(list(self.hand))
        jokers = counted['J']
        # NO JOKERS
        if jokers == 0:
            if len(counted) == 1:
                return top # Five of a Kind
            if len(counted) == 2:
                if 4 in counted.values():
                    return top - 1 # Four of a Kind
                elif 3 in counted.values() and 2 in counted.values():
                    return top - 2 # Full House
                else:
                    raise NotImplementedError(f"hand_type error 2 {self.hand}")
            if len(counted) == 3:
                if 3 in counted.values():
                    return top - 3 # Three of a Kind
                elif list(sorted(counted.values())) == [1,2,2]:
                    return top - 4 # Two Pair
                else:
                    raise NotImplementedError(f"hand_type error 3 {self.hand}")
            if len(counted) == 4:
                if list(sorted(counted.values())) == [1,1,1,2]:
                    return top - 5 # One Pair
                else:
                    raise NotImplementedError(f"hand_type error 4 {self.hand}")
            if len(counted) == 5:
                return top - 6
            raise NotImplementedError(f"hand_type error 5 {self.hand}")
        del counted['J'] # clear jokers
        if len(counted) == 0 or len(counted) == 1:
            return top  # Five of a Kind
        if len(counted) == 2:
            if 4-jokers in counted.values():
                return top - 1  # Four of a Kind
            elif jokers == 1 and list(sorted(counted.values())) == [2,2]:
                return top - 2  # Full House
            else:
                raise NotImplementedError(f"joker hand_type error 2 {self.hand}")
        if len(counted) == 3:
            if jokers == 2:
                return top - 3  # Three of a Kind
            elif jokers == 1 and 2 in counted.values():
                return top - 3  # Three of a Kind
            else:
                raise NotImplementedError(f"joker hand_type error 3 {self.hand}")
        if len(counted) == 4:
            return top - 5  # One Pair
        raise NotImplementedError(f"joker hand_type error 5 {self.hand}")

    def __eq__(self, other):
        return self.hand == other.hand

    def __lt__(self, other):
        return self.__cmp__(other) < 0
    def __cmp__(self, other):
        types_cmp = cmp(self.hand_type, other.hand_type)
        if types_cmp != 0:
            return types_cmp
        for sc, oc in zip(list(self.hand), list(other.hand)):
            compared_cards = cmp_card2(sc, oc)
            if compared_cards != 0:
                return compared_cards
        logger.debug(f"Two cards considered equal: {self.hand} - {other.hand}")
        return 0



if __name__ == '__main__':
    main()
