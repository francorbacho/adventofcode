#!/usr/bin/env python

import fileinput

lines = [line for line in fileinput.input()]

path = lines[0].strip()
patterns = lines[2:]
patterns = [p.replace('=', '') for p in patterns]
patterns = [p.replace('(', '') for p in patterns]
patterns = [p.replace(')', '') for p in patterns]
patterns = [p.replace(',', '') for p in patterns]
patterns = [[n.strip() for n in p.split(' ') if n.strip() != ''] for p in patterns]
patterns = { k: [lhs, rhs] for [k, lhs, rhs] in patterns }

cnode = 'AAA'
ipath = 0
steps = 0
while cnode != 'ZZZ':
    side = 0 if path[ipath] == 'L' else 1
    cnode = patterns[cnode][side]
    steps += 1
    ipath = (ipath + 1) % len(path)
    print(f"cnode :: {cnode}")

print(f"steps :: {steps}")
