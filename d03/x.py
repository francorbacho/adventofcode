import numpy as np

symbols = "#%&*+-/=@$"
digits = "0123456789"

def dbg(lines):
    for y, line in enumerate(lines):
        print("".join(line), end=" ")
        for x, c in enumerate(line):
            print("T" if c in digits and has_adjacent(lines, x, y) else ".", end="")
        print()

def has_adjacent(lines, x, y, values=symbols):
    return get_adjacent(lines, x, y, values) != []

def get_adjacent(lines, x, y, values=symbols):
    res = []
    l = len(lines)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            cx = dx + x
            cy = dy + y
            if 0 <= cy < len(lines) and 0 <= cx < len(lines[cy]) and lines[cy][cx] in values:
                res += [(cx, cy)]
    return res

with open("input.txt", "r") as f:
    lines = f.readlines()
    lines = [list(line.strip()) for line in lines]

total = 0
for y, line in enumerate(lines):
    number = ""
    within_number = False
    found_adjacent_symbol = False
    for x, c in enumerate(line + ['.']):
        if c in digits:
            # within number
            within_number = True
            found_adjacent_symbol = found_adjacent_symbol or has_adjacent(lines, x, y)
            number += c
        elif within_number:
            # number finished
            if found_adjacent_symbol:
                print(number, end=" ")
                total += int(number)
            number = ""
            within_number = False
            found_adjacent_symbol = False
    print()

print(total)

print('part two:')

def rewind_number(lines, x, y):
    while 0 < x and lines[y][x - 1] in digits:
        x -= 1
    return x, y

def parse_number(lines, x, y):
    num = lines[y][x]
    while x < len(lines[y]) - 1 and lines[y][x + 1] in digits:
        x += 1
        num += lines[y][x]
    return int(num)

def parse_adjacent(lines, nums):
    nums = [rewind_number(lines, x, y) for x, y in nums]
    # remove redundant
    nums = list(set(nums))
    nums = [parse_number(lines, x, y) for x, y in nums]
    return nums

total = 0
for y, line in enumerate(lines):
    for x, c in enumerate(line + ['.']):
        if c != '*':
            continue
        nums = get_adjacent(lines, x, y, digits)
        nums = parse_adjacent(lines, nums)
        if len(nums) != 2:
            continue
        total += np.product(nums)
print(total)
