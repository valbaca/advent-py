from advent.elf import in_file, lines_blank_grouped


def main():
    groups_input = lines_blank_grouped(in_file(__file__))
    print(groups_input)
    print(sum(map(any_answered_yes_count, groups_input)))
    print(sum(map(all_answered_yes_count, groups_input)))


def any_answered_yes_count(group):
    yes_set = set()
    for ans in group:
        yes_set.update(list(ans))
    return len(yes_set)


def all_answered_yes_count(group):
    yes_set = set(list(group[0]))
    for ans in group:
        yes_set.intersection_update(list(ans))
    return len(yes_set)


if __name__ == '__main__':
    main()
