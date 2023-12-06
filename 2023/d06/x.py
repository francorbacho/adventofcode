#!/usr/bin/env python

import fileinput

lines = [line for line in fileinput.input()]
times = [int(number.strip()) for number in lines[0].split(':')[1].split(' ') if number.strip() != '']
dists = [int(number.strip()) for number in lines[1].split(':')[1].split(' ') if number.strip() != '']

def part1():
    result = 1
    for time, dist in zip(times, dists, strict=True):
        accum = 0
        for hold in range(0, time):
            if dist < hold * (time - hold):
                accum += 1
        result *= accum
    return result

print(f"part one :: {part1()}")

def part2():
    time = int("".join(str(time) for time in times))
    dist = int("".join(str(dist) for dist in dists))
    accum = 0
    for hold in range(0, time):
        if dist < hold * (time - hold):
            accum += 1
    return accum

print(f"part two :: {part2()}")
