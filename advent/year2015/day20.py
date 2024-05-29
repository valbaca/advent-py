import math
from itertools import count

# TIL:
# python has the usual % operator
# keyword args w/ defaults make it super easy to write flexible functions

BEGIN = 700000


def factors(n, cutoff=None):
    factors = []
    for factor in range(1, math.ceil(math.sqrt(n))):
        d, m = divmod(n, factor)
        if m == 0:
            factors.append(factor)
            factors.append(math.trunc(d))
    if cutoff:
        factors = filter(lambda x: x >= cutoff, factors)
    return factors


def part1(tgt):
    max = 0
    for hnum in count(BEGIN):
        facts = factors(hnum)
        presents = sum(facts) * 10
        # if presents > max:
        #     max = presents
        #     print(f"currently at max={max}")
        if presents >= tgt:
            return hnum


def part2(tgt):
    # get the factors, discard factors where factor * 50 < num
    max = 0
    for hnum in count(BEGIN):
        facts = factors(hnum, cutoff=hnum // 50)
        presents = sum(facts) * 11
        # if presents > max:
        #     max = presents
        #     print(f"currently at max={max} for {hnum} facts={facts}")
        if presents >= tgt:
            return hnum


def main():
    print(factors(20))
    print(part1(150))
    print(part1(33100000))  # 776160
    # print(part2(10000))
    print(part2(33100000))  # 786240


if __name__ == "__main__":
    main()
