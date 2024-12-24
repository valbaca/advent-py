from advent import elf


# thankfully having done enough advent, 2d grids are the bread-and-butter
# Honestly surprised I didn't have a "radiate" function already, but was simple enough to write
# Second part was a bit tricky but when I realized, 1) we only go in diagonals and 2) I didn't originally have a way to
# tell "SAM" from "MAS". Simple changes fixed those though: only go in diagonals and use a Set

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


DIRS = [
    (0, 1),  # Right
    (1, 1),  # Down-right diagonal
    (1, 0),  # Down
    (-1, 1),  # Up-right diagonal
    (0, -1),  # Left
    (-1, -1),  # Up-left diagonal
    (-1, 0),  # Up
    (1, -1)  # Down-left diagonal
]


# Goes "out" from one point, like a ray
def radiate(grid, start_row, start_col, length):
    rows, cols = len(grid), len(grid[0])
    results = []

    for dr, dc in DIRS:
        current_path = []
        for step in range(length):  # Include the starting point and max_distance
            r, c = start_row + step * dr, start_col + step * dc
            if 0 <= r < rows and 0 <= c < cols:  # Ensure within bounds
                current_path.append(grid[r][c])
            else:
                break  # Stop if out of bounds
        results.append(current_path)

    return results


def part1(lines):
    grid = [list(line) for line in lines]
    count = 0
    target = "XMAS"
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            paths = radiate(grid, row, col, length=4)
            count += len([1 for path in paths if "".join(path) == target])
    return count


X_DIRS = [
    (1, 1),  # Down-right diagonal
    (-1, 1),  # Up-right diagonal
]


# Goes in both directions (made generic even though we only go "out" one character for this puzzle
def xradiate(grid, start_row, start_col, length):

    rows, cols = len(grid), len(grid[0])
    results = []

    for dr, dc in X_DIRS:
        current_path = []  # Holds values radiating out in both directions

        # Radiate in the positive direction
        for step in range(length):
            r, c = start_row + step * dr, start_col + step * dc
            if 0 <= r < rows and 0 <= c < cols:
                current_path.append(grid[r][c])
            else:
                break  # Stop if out of bounds

        # Radiate in the negative direction (backward along the same line)
        for step in range(1, length):  # Start at 1 to avoid duplicating the center
            r, c = start_row - step * dr, start_col - step * dc
            if 0 <= r < rows and 0 <= c < cols:
                current_path.insert(0, grid[r][c])
            else:
                break  # Stop if out of bounds

        results.append(current_path)

    return results

def part2(lines):
    grid = [list(line) for line in lines]
    count = 0
    mas_set = set(list("MAS")) # using a set to avoid flipping MAS into SAM
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            paths = xradiate(grid, row, col, length=2)
            path_sets = [set(path) for path in paths] # using set to have MAS==SAM
            if grid[row][col] == "A" and path_sets.count(mas_set) >= 2: # only count "out" from the A
                count += 1

    return count


if __name__ == '__main__':
    main()
