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
