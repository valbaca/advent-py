import math
import sys
from enum import Enum
from dataclasses import dataclass

# TIL:
# - globals are just defined and can be read
# - to assign to globals, you need to include `global name_of_global` so a local var isn't made
# - Enums are straightforward, they have .name and .value
# - Important part of the backtrack algorithm was cutting off never-ended paths, the "invalid" check is crucial
# - pypy is much faster! pypy took 7.6s, python3 took 95.5s => ~11.5x faster!

backtracking = """
def backtrack(args):
    if invalid(args) or bad(args):
        return
    if solution(args) and is_best_solution(args):
        handle_solution(args)   # usually update global or arg that's a wrapping reference
    for options in generate_options(args):
        make_move(option, args)
        backtrack(args) # recursion
        undo_move(option, args)
"""

hard_mode = False


class Spell(Enum):
    MagicMissile = ("Magic Missile", 53)
    Drain = ("Drain", 73)
    Shield = ("Shield", 113)
    Poison = ("Poison", 173)
    Recharge = ("Recharge", 229)


@dataclass
class You:
    hp: int
    mana: int
    armor: int

    def get_hit(self, dmg):
        self.hp -= max(dmg - self.armor, 1)

    def dead(self):
        return self.hp <= 0


@dataclass
class Boss:
    hp: int
    dmg: int

    def dead(self):
        return self.hp <= 0


def apply(you, boss, effects):
    next_turn_effects = []
    for effect in effects:
        (es, duration) = effect
        if es == Spell.Shield:
            you.armor = 7
        elif es == Spell.Poison:
            boss.hp -= 3
        elif es == Spell.Recharge:
            you.mana += 101

        if duration > 1:
            next_turn_effects.append((es, duration - 1))
        elif es == Spell.Shield and duration == 1:
            you.armor = 0
    return you, boss, next_turn_effects


failure = "failure"
stalemate = "stalemate"
victory = "victory"

def battle(spells, min_found):
    # Execute the spells in order
    you = You(50, 500, 0)
    boss = Boss(58, 9)
    effects = []
    mana_spent = 0
    for spell in spells:
        if hard_mode:
            you.get_hit(1)
            if you.dead():
                return failure, -1
        # each loop is one round: effects, you cast, effects again, boss hits back
        you, boss, effects = apply(you, boss, effects)
        if boss.dead():
            return victory, mana_spent
        spell_cost = spell.value[1]
        mana_spent += spell_cost
        if mana_spent > min_found:
            return failure, -1  # quit while youre ahead
        you.mana -= spell_cost
        active_effect_spells = [e[0] for e in effects]
        if spell in active_effect_spells or you.mana < 0:
            return failure, -1
        # cast spell!
        if spell == Spell.MagicMissile:
            boss.hp -= 4
        elif spell == Spell.Drain:
            you.hp += 2
            boss.hp -= 2
        elif spell == Spell.Shield:
            effects.append((spell, 6))
        elif spell == Spell.Poison:
            effects.append((spell, 6))
        elif spell == Spell.Recharge:
            effects.append((spell, 5))

        # End of your turn
        if boss.dead():
            return victory, mana_spent

        # Boss' turn
        you, boss, effects = apply(you, boss, effects)
        if boss.dead():
            return victory, mana_spent
        you.get_hit(boss.dmg)
        # End of boss' turn
        if you.dead():
            return failure, -1
    return stalemate, mana_spent

def run(spells, min_found):
    result, cost = battle(spells, min_found)
    if result == failure or (result == victory and cost >= min_found):
        return min_found
    if result == victory and cost < min_found:
        return cost
    for spell in Spell:
        sub_min_found = run(spells + [spell], min_found)
        if sub_min_found < min_found:
            min_found = sub_min_found
    return min_found

def part1(spells):
    print(run([], math.inf)) 

def main():
    global hard_mode
    print("part 1")
    part1([])
    print("part 2")
    hard_mode = True
    part1([])


if __name__ == "__main__":
    main()
