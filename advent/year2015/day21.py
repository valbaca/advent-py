from dataclasses import dataclass
from itertools import permutations
from sys import maxsize

from advent.elf import read_lines, septoi

# Notes:
# - dataclass and itertools are great
# - repeating `self` in classes is tedious, just like `this` in JavaScript (Maybe I miss Ruby/Crystal)
# - Using the Null Object Item.NO_ITEM made it simple to not have to deal with None
# - Getting list of lines is just list(open(filename))! doesn't close, but for this stuff whatever
class Char:
    def __init__(self, name, hp, dmg, armor):
        self.name = name
        self.full_hp = hp
        self.hp = hp
        self.dmg = dmg
        self.armor = armor

    def __repr__(self):
        return f"[Char(name={self.name},hp={self.hp},dmg={self.dmg},armor={self.armor}"

    def is_dead(self):
        return self.hp <= 0

    def beats(self, other):
        while True:
            self.hit(other)
            if other.is_dead():
                # print(f"{self.name} wins!")
                return True
            other.hit(self)
            if self.is_dead():
                # print(f"{other.name} wins!")
                return False

    def hit(self, other):
        dealt = max(self.dmg - other.armor, 1)
        # print(f"{self.name} hits {other.name} for {dealt} dmg")
        other.hp -= dealt
        # print(f"{other.name} is now at {other.hp} hp")

    def reset(self):
        self.hp = self.full_hp
        self.dmg = 0
        self.armor = 0

    def reset_hp(self):
        self.hp = self.full_hp

    def equip(self, items):
        for item in items:
            self.armor += item.armor
            self.dmg += item.dmg


@dataclass
class Item:
    name: str
    cost: int
    dmg: int
    armor: int

    @staticmethod
    def from_line(s):
        sp = septoi(s,  r"[^a-zA-Z0-9_+-]")
        name, cost, dmg, armor = sp
        return Item(name, int(cost), int(dmg), int(armor))


Item.NO_ITEM = Item("NO_ITEM", 0, 0, 0)


def test1():
    you = Char("You", 8, 5, 5)
    boss = Char("Boss", 12, 7, 2)
    you.beats(boss)


def build_items():
    lines = read_lines(__file__)
    weapons = [Item.from_line(x) for x in lines[1:6]]
    armor = [Item.from_line(x) for x in lines[7:12]]
    rings = [Item.from_line(x) for x in lines[13:]]
    # print(weapons, armor, rings)
    armor.append(Item.NO_ITEM)
    rings.append(Item.NO_ITEM)
    rings.append(Item.NO_ITEM)
    ring_pairs = list(permutations(rings, 2))
    # print(list(ring_pairs))
    return weapons, armor, ring_pairs


def day1(you: Char, boss: Char):
    min_cost_found = maxsize
    weapons, armor, ring_pairs = build_items()

    for w in weapons:
        for a in armor:
            for left, right in ring_pairs:
                items = [w, a, left, right]
                total = sum([x.cost for x in items])
                if total < min_cost_found:
                    you.equip(items)
                    if you.beats(boss):
                        min_cost_found = total
                        # print(f"New min cost! {min_cost_found} items={items}")
                    you.reset()
                    boss.reset_hp()
    print("Lowest found:", min_cost_found)


def day2(you: Char, boss: Char):
    max_cost_found = -1
    weapons, armor, ring_pairs = build_items()

    for w in weapons:
        for a in armor:
            for left, right in ring_pairs:
                items = [w, a, left, right]
                total = sum([x.cost for x in items])
                if total > max_cost_found:
                    you.equip(items)
                    if not you.beats(boss):
                        max_cost_found = total
                        # print(f"New max cost! {max_cost_found} items={items}")
                    you.reset()
                    boss.reset_hp()
    print("Highest found:", max_cost_found)


def main():
    test1()
    you, boss = Char("You", 100, 0, 0), Char("Boss", 103, 9, 2)
    day1(you, boss)
    day2(you, boss)


if __name__ == "__main__":
    main()