from advent import elf


# This was a tricky one!
# The first part was fun and easy. Simply split out the list into two (files and empty) but realized it wasn't going to work easily with part two
# Switched over to a (linked) list approach which worked good enough
# Had to deal with a lot of left-right index/pointers which I generally try to avoid

def main():
    test_lines = elf.read_lines(__file__, test=True)
    lines = elf.read_lines(__file__)
    print("Part 1 (test):")
    print(part1(test_lines))
    print("Part 1:")
    print(part1(lines))
    print("Part 2 (test):")
    print(part2(test_lines))
    print("Part 2:")
    print(part2(lines))


# files, free-space, ...

def part1(lines):
    xs = [int(ch) for ch in lines[0]]
    files = xs[::2]
    pfiles = 0
    free = xs[1::2]
    pfree = 0
    check, cptr = 0, 0
    while any(v > 0 for v in files):
        # eat from the files
        while pfiles < len(files) and files[pfiles] > 0:
            check += cptr * pfiles
            files[pfiles] -= 1
            cptr += 1
        pfiles += 1

        # fill in free spaces by eating from the end
        while pfree < len(free) and free[pfree] > 0:
            # find the right-most non-zero
            end_pfiles = index_right_nonzero(files)
            if end_pfiles is None:
                # no more files
                break
            check += cptr * end_pfiles
            files[end_pfiles] -= 1
            cptr += 1
            free[pfree] -= 1
        pfree += 1
    return check


def index_right_nonzero(lst):
    for i in reversed(range(len(lst))):
        if lst[i] != 0:
            return i
    return None


def part2(lines):
    # starting over with a linked list of tuples
    # (id, size), id is -1 for empty space
    fds = [] # file descriptors, tuples of (id?, size) where id is None if it's empty space
    for idx, ch in enumerate(lines[0]):
        if idx % 2 == 0:

            fds.append((idx//2, int(ch)))
        else:
            fds.append((None, int(ch)))

    # compact
    while True:
        move = find_move(fds)
        if move is None:
            break
        # execute move
        empty_idx, file_idx = move
        empty_size = fds[empty_idx][1]
        file_id, file_size = fds[file_idx]

        fds[file_idx] = (None, file_size) # simply replace with empty file
        del fds[empty_idx]
        if empty_size > file_size:
            fds.insert(empty_idx, (None, empty_size-file_size)) # left-over space
        fds.insert(empty_idx, (file_id, file_size))

    # checksum
    ptr = 0
    c = 0
    check = 0
    while ptr < len(fds):
        fid, size = fds[ptr]
        if fid is None:
            c += size
        else:
            while size > 0:
                check += c * fid
                c += 1
                size -= 1
        ptr += 1
    return check

def find_move(fds):
    for j in reversed(range(len(fds))):
        file_id, file_size = fds[j]
        if file_id is None:
            continue
        for i in range(j):
            empty_id, empty_size = fds[i]
            if empty_id is not None:
                continue
            if 0 < file_size <= empty_size:
                return i, j
    return None


if __name__ == '__main__':
    main()
