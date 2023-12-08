#!/usr/bin/env python
# 12405506477569092685163520 is too high
#     2393037514963173743280 is too high

import fileinput
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

lines = [line for line in fileinput.input()]

path = lines[0].strip()
patterns = lines[2:]
patterns = [p.replace('=', '') for p in patterns]
patterns = [p.replace('(', '') for p in patterns]
patterns = [p.replace(')', '') for p in patterns]
patterns = [p.replace(',', '') for p in patterns]
patterns = [[n.strip() for n in p.split(' ') if n.strip() != ''] for p in patterns]
patterns = { k: [lhs, rhs] for [k, lhs, rhs] in patterns }

cnodes = [p for p in patterns if p.endswith('A')]
ipath = 0
steps = 0

z_apparences = [0 for _ in cnodes]
loopback_steps_z = [0 for _ in cnodes]
step_last_z = [0 for _ in cnodes]

while not all(map(lambda x: x > 1, z_apparences)):
    side = 0 if path[ipath] == 'L' else 1
    for i, cnode in enumerate(cnodes):
        cnodes[i] = patterns[cnode][side]
        if cnodes[i].endswith('Z'):
            z_apparences[i] += 1
            loopback_steps_z[i] = steps - step_last_z[i]
            step_last_z[i] = steps
    steps += 1
    ipath = (ipath + 1) % len(path)

res = 1
for lsteps in loopback_steps_z:
    res = lcm(res, lsteps)

print(f"steps :: {res}")
