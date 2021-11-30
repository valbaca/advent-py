from advent import elf


def main():
    # [Card PK, Door PK]
    pub_keys = [5764801, 17807724]
    print(part1(pub_keys))
    pub_keys = [335121, 363891]
    print(part1(pub_keys))


DAY = 20201227


def transform(n, subj=7):
    val = n * subj
    return val % DAY
    # return val if val < DAY else (val % DAY)


def part1(pks):  # public keys
    print(f"public keys = {pks}")
    loop = 0
    loop_sizes = [None, None]
    # ekls = [{}, {}]  # encryption keys -> loops
    val = 1
    while loop_sizes[0] is None or loop_sizes[1] is None:
        loop += 1
        val = transform(val)
        for i in range(2):
            if val == pks[i] and loop_sizes[i] is None:
                loop_sizes[i] = loop
    print(f"loop sizes = {loop_sizes}")
    ans = []
    val = 1
    for i in range(loop_sizes[1]):
        val = transform(val, pks[0])
    ans.append(val)

    val = 1
    for i in range(loop_sizes[0]):
        val = transform(val, pks[1])
    ans.append(val)
    return ans


if __name__ == '__main__':
    main()
