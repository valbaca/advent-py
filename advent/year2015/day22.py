import math
from dataclasses import dataclass
from enum import Enum

# TIL:
# - globals are just defined and can be read
# - to assign to globals, you need to include `global name_of_global` so a local var isn't made
# - Enums are straightforward, they have .name and .value
# - Important part of the backtrack algorithm was cutting off never-ended paths, the "invalid" check is crucial
# - pypy is much faster! pypy took 7.6s, python3 took 95.5s => ~11.5x faster!
# - (Sep 2022) Improved speed even more by not casting all spells in succession; using state and clones for backtracking.

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


@dataclass
class State:
    you: You
    boss: Boss
    effects: dict
    mana_spent: int

    def clone(self):
        return State(
            You(self.you.hp, self.you.mana, self.you.armor),
            Boss(self.boss.hp, self.boss.dmg),
            self.effects.copy(),
            self.mana_spent
        )


def apply(state):
    you, boss, effects = state.you, state.boss, state.effects
    to_del = []
    for sp, dur in effects.items():
        if sp == Spell.Shield:
            if dur == 1:
                you.armor = 0
            else:
                you.armor = 7
        elif sp == Spell.Poison:
            boss.hp -= 3
        elif sp == Spell.Recharge:
            you.mana += 101
        if dur == 1:
            to_del.append(sp)
    for del_spell in to_del:
        del effects[del_spell]
    for sp in effects.keys():
        effects[sp] -= 1
    return effects


failure = "failure"
stalemate = "stalemate"
victory = "victory"


# apply the spell and execute one round of combat, returns result and resulting state
def apply_spell(state: State, spell, min_found):
    if hard_mode:
        state.you.get_hit(1)
        if state.you.dead():
            return failure, None
    # each loop is one round: effects, you cast, effects again, boss hits back
    state.effects = apply(state)
    if state.boss.dead():
        return victory, state
    spell_cost = spell.value[1]
    state.mana_spent += spell_cost
    if state.mana_spent > min_found:
        return failure, None  # quit while you're behind
    state.you.mana -= spell_cost
    if state.you.mana < 0 or (state.effects.get(spell) and state.effects[spell] > 0):
        return failure, None
    # cast spell!
    if spell == Spell.MagicMissile:
        state.boss.hp -= 4
    elif spell == Spell.Drain:
        state.you.hp += 2
        state.boss.hp -= 2
    elif spell == Spell.Shield:
        state.effects[spell] = 6
    elif spell == Spell.Poison:
        state.effects[spell] = 6
    elif spell == Spell.Recharge:
        state.effects[spell] = 5

    # End of your turn
    if state.boss.dead():
        return victory, state

    # Boss' turn
    state.effects = apply(state)
    if state.boss.dead():
        return victory, state
    state.you.get_hit(state.boss.dmg)
    # End of boss' turn
    if state.you.dead():
        return failure, None
    return stalemate, state


def combat(state: State, min_found):
    for spell in Spell:
        result, restate = apply_spell(state.clone(), spell, min_found)
        if result == failure or (result == victory and restate.mana_spent >= min_found):
            continue
        if result == victory and restate.mana_spent < min_found:
            min_found = restate.mana_spent
            continue
        # else stalemate, continue depth search
        sub_min_found = combat(restate, min_found)
        if sub_min_found < min_found:
            min_found = sub_min_found
    return min_found


def part1():
    # init_state = State(You(10, 250, 0), Boss(13, 8), {}, 0) # example
    init_state = State(You(50, 500, 0), Boss(58, 9), {}, 0)
    print(combat(init_state, math.inf))


def main():
    global hard_mode
    print("part 1")
    part1()
    print("part 2")
    hard_mode = True
    part1()


if __name__ == "__main__":
    main()
