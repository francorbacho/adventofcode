#!/usr/bin/env python

import fileinput
import copy
import numpy as np
import itertools

def expand(world: list[list[str]]) -> list[list[str]]:
    # expand rows
    world = [line if "#" in line else f"{line}\n{line}" for line in world]
    world = "\n".join(line for line in world)
    world = [[*line] for line in world.split("\n")]
    world = np.array(world)

    # expand columns
    for col in range(len(world[0]) - 1, 0, -1):
        if any(map(lambda x: x == "#", world[:, col])):
            continue
        world = np.insert(world, col, axis=1, values=world[:, col])

    return [list(line) for line in world]

def count_galaxies(world: list[list[str]]) -> set[(int, int)]:
    res = set()
    for row, line in enumerate(world):
        tmp = "".join(line)
        while "#" in tmp:
            col = tmp.find("#")
            if col == -1:
                continue
            tmp = tmp.replace("#", "@", 1)
            res.add((row, col))
    return res

def calculate_dist(src: tuple[int, int], dst: tuple[int, int]) -> int:
    dist = abs(src[0] - dst[0]) + abs(src[1] - dst[1])
    return dist

def part1():
    lines = [line.strip() for line in fileinput.input() if line.strip() != ""]
    world = expand(lines)
    galax = count_galaxies(world)
    dists = [calculate_dist(*pair) for pair in itertools.combinations(galax, 2)]

    res = sum(dists)

    print(f"res :: {res}")

part1()
