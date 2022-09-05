target_row = 2978
target_col = 3083

def part1():
    r, c, val = 1, 1, 20151125
    while True:
        if r == target_row and c == target_col:
            return val
        r, c, val = next(r, c, val)

def next(r, c, val):
    if r == 1:
        r = c + 1
        c = 1
    else:
        r -= 1
        c += 1
    return r, c, (val * 252533) % 33554393

def part2():
    return "Happy Advent! 2015 done!!!"

if __name__ == "__main__":
    print(part1())
    print(part2())
