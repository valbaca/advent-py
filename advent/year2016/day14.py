import hashlib
from collections import deque


def main():
    # test_lines = elf.read_lines(__file__, test=True)
    print("Part 1 (test):", part1("abc"))

    # lines = elf.read_lines(__file__)
    print("Part 1:", part1("yjdafjpo"))
    print("Part 2:", part2("yjdafjpo"))


def md5(s):
    return hashlib.md5(s).hexdigest()


def get_triplet(s):
    for i in range(len(s) - 2):
        if s[i] == s[i + 1] == s[i + 2]:
            return s[i]
    return None


def get_quints(s):
    quints = set()
    for i in range(len(s) - 4):
        if s[i] == s[i + 1] == s[i + 2] == s[i + 3] == s[i + 4]:
            quints.add(s[i])
    return quints if quints else None


def calc(salt, i, hash_n):
    hash = (salt + str(i))
    for _ in range(hash_n):
        hash = md5(hash.encode("utf-8"))
    triplet = get_triplet(hash)
    quints = get_quints(hash)
    return hash, triplet, quints


def part1(salt, key_wanted=64, hash_n=1):
    dq = deque()
    for i in range(1000):
        dq.append(calc(salt, i, hash_n))
    last_key = None
    i = 0
    while key_wanted > 0:
        # print(i)
        hash, triplet, quints = dq.popleft()
        if triplet:
            # print(f"{i}: {triplet=}")
            for other_hash, _, other_quints in dq:
                if other_quints and triplet in other_quints:
                    key_wanted -= 1
                    # print(f"key found {i}")
                    last_key = i + 1
                    break
        i += 1
        dq.append(calc(salt, i + 1000, hash_n))
    return last_key


def part2(salt):
    return part1(salt, key_wanted=64, hash_n=2017)


if __name__ == '__main__':
    main()
