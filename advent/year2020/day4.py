import re
from typing import AnyStr

from advent.elf import in_file, strip_lines


def lines_to_passports(lines):
    # collect into arrays separated by the blank line
    passports = [[]]
    for line in lines:
        if line:
            passports[-1].append(line)
        else:
            passports.append([]) # blank line = new passport
    # collect passports into a single string
    passports = [str.join(' ', arr) for arr in passports]
    # now we can take it apart and create objects out of it
    passports = [re.split(r"[\s:]", s) for s in passports]
    return map(list_to_passport, passports)


def list_to_passport(plist):
    passport = {}
    for i in range(0, len(plist), 2):
        k, v = plist[i], plist[i + 1]
        passport[k] = v
    return passport


def has_all_keys(keys):
    return set(keys) >= set("byr iyr eyr hgt hcl ecl pid".split())


def part1(lines):
    passports = lines_to_passports(lines)
    print(len([p for p in passports if has_all_keys(p.keys())]))


def valid_height(h: AnyStr):
    if h.endswith("cm"):
        return int(h[:-2]) in range(150, 193 + 1)
    elif h.endswith("in"):
        return int(h[:-2]) in range(59, 76 + 1)
    return False


def valid_hair(h):
    return re.fullmatch(r"#[0-9a-f]{6}", h)


def valid_eye(e):
    return e in 'amb blu brn gry grn hzl oth'.split()


def valid_pid(p):
    return re.fullmatch(r"[0-9]{9}", p)


def valid_passport(p):
    return (has_all_keys(p.keys())
            and (1920 <= int(p["byr"]) <= 2002)
            and (2010 <= int(p["iyr"]) <= 2020)
            and (2020 <= int(p["eyr"]) <= 2030)
            and valid_height(p["hgt"])
            and valid_hair(p["hcl"])
            and valid_eye(p["ecl"])
            and valid_pid(p["pid"]))


def part2(lines):
    passports = lines_to_passports(lines)
    print(len([p for p in passports if valid_passport(p)]))


def main():
    lines = strip_lines(in_file(__file__))
    part1(lines)
    part2(strip_lines("day4-invalid.txt"))
    part2(strip_lines("day4-valid.txt"))
    part2(lines)


if __name__ == '__main__':
    main()
