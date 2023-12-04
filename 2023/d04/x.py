#!/usr/bin/env python

import fileinput
import re

def ints(inp: str):
    return [int(x.group(0)) for x in re.finditer(r'\d+', inp)]

lines = [line.strip() for line in fileinput.input() if line.strip() != '']
lines = [line.split(':')[1] for line in lines]
lines = [line.split('|') for line in lines]
lines = [(ints(line[0]), ints(line[1])) for line in lines]

score = 0
for winning, mine in lines:
    matching = sum(int(scratch in winning) for scratch in mine)
    if matching != 0:
        score += 2 ** (matching - 1)

print(f"\n".join(str(line) for line in lines))
print(f"score :: {score}")

def part2(lines, lo, hi, indent = 0):
    total = hi - lo
    for i, (winning, mine) in enumerate(lines[lo:hi]):
        matching = sum(int(scratch in winning) for scratch in mine)
        # print("\t" * indent + f"card #{1 + i + lo} :: {matching}, so :: {lo + 1} to {lo + 1 + matching}")
        total += part2(lines, i + lo + 1, i + lo + 1 + matching, indent + 1)
    return total

print(f"scratchcards :: {part2(lines, 0, len(lines))}")
