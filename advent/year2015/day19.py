from collections import defaultdict
from random import shuffle

# https://adventofcode.com/2015/day/19
# TIL: sometimes greedy, brute-force, or random just works

IN = """
e => H
e => O
H => HO
H => OH
O => HH
"""

IN_ACTUAL = """
Al => ThF
Al => ThRnFAr
B => BCa
B => TiB
B => TiRnFAr
Ca => CaCa
Ca => PB
Ca => PRnFAr
Ca => SiRnFYFAr
Ca => SiRnMgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CRnAlAr
H => CRnFYFYFAr
H => CRnFYMgAr
H => CRnMgYFAr
H => HCa
H => NRnFYFAr
H => NRnMgAr
H => NTh
H => OB
H => ORnFAr
Mg => BF
Mg => TiMg
N => CRnFAr
N => HSi
O => CRnFYFAr
O => CRnMgAr
O => HP
O => NRnFAr
O => OTi
P => CaP
P => PTi
P => SiRnFAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg
"""

START = "CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr"


def parse(lines):
    d = defaultdict(list)
    for line in lines.splitlines():
        splits = line.split(" ")
        if len(splits) == 3:
            (key, _, val) = splits
            d[key].append(val)
    return d


def gen_replacements(s, replacements):
    seen = set()
    for i, ch in enumerate(s):
        for val in replacements[ch]:
            replaced = s[:i] + val + s[i + 1:]
            seen.add(replaced)
        # handle the two-char cases (not great but works)
        prefix = s[i: i + 2]
        for val in replacements[prefix]:
            replaced = s[:i] + val + s[i + 2:]
            seen.add(replaced)
    return seen


def p1helper(s, repl):
    return len(gen_replacements(s, parse(repl)))


def build_red(repl):
    red = []
    for short, longs in repl.items():
        for long in longs:
            red.append((long, short))
    return red


def p2attempt2(tgt, repl):
    # repl is short -> long, we want list of [(long, short), ...] sorted by longest
    red = build_red(repl)
    atom = tgt  # type: str
    count = 0
    while atom != "e":
        shrunk = False
        for long, short in red:
            temp = atom.replace(long, short)
            if temp != atom:
                count += atom.count(long)
                atom = temp
                # print(len(atom), atom)
                shrunk = True
                break
        if not shrunk:  # then reset and try another order...this is dumb
            atom = tgt
            count = 0
            shuffle(red)
    return count


def part1():
    print("part 1:")
    # print(p1helper("HOH", IN))
    # print(p1helper("HOHOHO", IN))

    print(p1helper(START, IN_ACTUAL))


def part2():
    print("part 2:")
    # print(p2attempt2("HOH", parse(IN)))
    # print(p2attempt2("HOHOHO", parse(IN)))

    print(p2attempt2(START, parse(IN_ACTUAL)))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
