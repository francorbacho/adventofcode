#!/usr/bin/env python

import fileinput
import sys

def get_connections(rowcol: tuple[int, int], pipe: str) -> set[tuple[int, int]]:
    row, col = rowcol
    connections = set()
    if pipe in "|LJ":
        # north
        connections.add((row - 1, col))
    if pipe in "|7F":
        # south
        connections.add((row + 1, col))
    if pipe in "-LF":
        # east
        connections.add((row, col + 1))
    if pipe in "-J7":
        # west
        connections.add((row, col - 1))
    # assert len(connections) > 0
    return connections

def visit(world: list[list[str]], rowcol: tuple[int, int], distmap: dict[tuple[int, int], int], steps: int = 0) -> None:
    row, col = rowcol
    if not (0 <= row < len(world)) or not (0 <= col < len(world[0])):
        return

    pipe = world[row][col]
    if pipe == '.':
        return

    if rowcol in distmap and distmap[rowcol] < steps:
            return
    distmap[rowcol] = steps
    for conn in get_connections(rowcol, pipe):
        visit(world, conn, distmap, steps + 1)

def find_starting_point(world: list[list[str]]) -> tuple[int, int]:
    for row, line in enumerate(lines):
        col = "".join(line).find("S")
        if col != -1:
            return row, col
    assert False, "Unable to find S"

def find_loopback_tiles(world: list[list[str]]) -> str:
    rowcol = find_starting_point(world)

    for pipe in "|-LJ7F":
        world[rowcol[0]][rowcol[1]] = pipe
        distmap = {}
        visit(lines, rowcol, distmap)
        key_of_highest = sorted(distmap, key=distmap.get, reverse=True)[0]
        if not all(map(lambda x: x in distmap, get_connections(rowcol, pipe))):
            continue
        conns = get_connections(rowcol, pipe)
        if any(rowcol not in get_connections(conn, world[conn[0]][conn[1]]) for conn in conns):
            continue
        return distmap, key_of_highest

    assert False, "unreachable"

def part1(world: list[list[str]]) -> int:
    distmap, furthest_point = find_loopback_tiles(world)
    return distmap[furthest_point]

def part2(world: list[list[str]]) -> int:
    distmap, _ = find_loopback_tiles(world)
    loopback = set(distmap)

    res = 0
    for row, line in enumerate(world):
        inside_loopback = False

        for col, c in enumerate(line):
            if (row, col) in loopback and c not in "-F7":
                inside_loopback = not inside_loopback
                continue
            if inside_loopback and (row, col) not in loopback:
                res += 1
    return res

sys.setrecursionlimit(15000)
lines = [[*line.strip()] for line in fileinput.input() if line.strip() != ""]

# print(f"part1 :: {part1(lines)}")
print(f"part2 :: {part2(lines)}")
