import re

from advent import elf

"""
I was honestly lucky that my part 1 solution also solved part 2 without any modifications.
"""


def main():
    lines = elf.lines_blank_grouped(elf.in_file(__file__))
    print(part1(lines))
    print(part2(lines))


def partial_match(all_rules, rule_num, s):
    rules = all_rules[rule_num]
    rem_strs = []
    for rule in rules:
        rems = [s]
        for rule_part in rule:
            new_rems = []
            if isinstance(rule_part, int):
                for rs in rems[:]:
                    part_match, part_rems = partial_match(all_rules, rule_part, rs)
                    if part_match:
                        new_rems.extend(part_rems)
            elif isinstance(rule_part, str):
                for rs in rems[:]:
                    if rs.startswith(rule_part):
                        new_rems.append(rs[len(rule_part):])
            else:
                raise RuntimeError("uh oh")
            rems = new_rems
        rem_strs.extend(rems)
    return len(rem_strs) > 0, rem_strs


def full_match(all_rules, rule_num, s):
    partial_matched, partial_rems = partial_match(all_rules, rule_num, s)
    return partial_matched and ('' in partial_rems)


def parse_rule(line):
    s = re.split(r"[\s:]", line)
    s = list(map(elf.safe_atoi, s))
    rules = [[]]
    for subs in s[1:]:
        if subs == '|':
            rules.append([])
        elif isinstance(subs, int):
            rules[-1].append(subs)
        elif subs:
            rules[-1].append(subs[1:-1])
    return s[0], rules


def parse_rules(lines):
    rules = {}
    for line in lines:
        rule_id, rule = parse_rule(line)
        rules[rule_id] = rule
    return rules


def part1(lines):
    rule_lines, messages = lines
    rules = parse_rules(rule_lines)
    # for m in messages:
    #     print(f"{m} => {full_match(rules, 0, m)}")
    return len([m for m in messages if full_match(rules, 0, m)])


def part2(lines):
    rule_lines, messages = lines
    rules = parse_rules(rule_lines)
    rules.update(parse_rules(["8: 42 | 42 8", "11: 42 31 | 42 11 31"]))
    # for m in messages:
    #     print(f"{m} => {full_match(rules, 0, m)}")
    return len([m for m in messages if full_match(rules, 0, m)])


if __name__ == '__main__':
    main()
