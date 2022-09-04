from advent.elf import read_lines

def part1(input):
    return len(see_say(input[0], 40))

def see_say(s, n):
    for _ in range(n):
        new = ""
        last = None
        for c in s:
            if c == last:
                count += 1
            else:
                if last is not None:
                    new += f"{count}{last}"
                count = 1
            last = c
        s = f"{new}{count}{last}"
    return new

def part2(input):
    return len(see_say(input[0], 50)) # whew! was worried it would go out of memory

if __name__ == "__main__":
    print(part1(read_lines(__file__)))
    print(part2(read_lines(__file__)))
