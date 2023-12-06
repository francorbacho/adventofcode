#!/usr/bin/env python

from __future__ import annotations

import fileinput
import math

class Conversion:
    def __init__(self, input_range_start: int, output_range_start: int, length: int) -> None:
        self.input_range_start = input_range_start
        self.output_range_start = output_range_start
        self.length = length

    def parse(string: str) -> Self:
        [ors, irs, length] = list(map(int, string.split(" ")))
        return Conversion(irs, ors, length)

    def can_do(self, inp: int) -> bool:
        return self.input_range_start <= inp < self.input_range_start + self.length

    def do(self, inp: int) -> int:
        assert self.can_do(inp)
        return self.output_range_start + inp - self.input_range_start

    def __repr__(self) -> str:
        return f"{self.input_range_start} -> {self.output_range_start} :: {self.length}"

class Map:
    def __init__(self, source: str, destination: str, conversions: list[Conversion]) -> None:
        self.source = source
        self.destination = destination
        self.conversions = conversions

    def parse(definitions: list[str]) -> Self:
        map_def = definitions[0][:-len(" map")]
        source, destination = map_def.split("-to-")
        conversions = [Conversion.parse(conv_def) for conv_def in definitions[1:]]
        return Map(source, destination, conversions)

    def convert(self, source: int) -> int:
        for conversion in self.conversions:
            if conversion.can_do(source):
                return conversion.do(source)
        return source

    def convert_range(self, start: int, length: int) -> list[tuple[int, int]]:
        res = []
        while True:
            if length == 0:
                break
            for conv in self.conversions:
                if conv.can_do(start):
                    output_start = conv.do(start)
                    output_length = min(length, conv.length - start + conv.input_range_start)
                    res.append((output_start, output_length))
                    start = start + output_length
                    length = length - output_length
                    break
            else:
                res.append((start, length))
                break
        return res

lines = [line.strip() for line in fileinput.input()]
lines = "\n".join(lines).split("\n\n")
lines = [line.split("\n") for line in lines]
seeds, *groups = lines

# parse seeds
seeds = seeds[0][len("seeds: "):]
seeds = list(map(int, seeds.split(" ")))
print(seeds)

# parse other things
maps = [Map.parse(defs) for defs in groups]

def process_seed(seed):
    source = seed
    for category in maps:
        destination = category.convert(source)
        source = destination
    return destination

def part1():
    min_loc = math.inf
    for i, seed in enumerate(seeds):
        destination = process_seed(seed)
        min_loc = min(min_loc, destination)
    return min_loc

print(f"part one :: {part1()}")

def process_range(maps: list[Map], imap: int, range_start: int, range_length: int) -> list[tuple[int, int]]:
    if imap == len(maps) - 1:
        return maps[imap].convert_range(range_start, range_length)
    res = []
    for (new_range_start, new_range_length) in maps[imap].convert_range(range_start, range_length):
        res += process_range(maps, imap + 1, new_range_start, new_range_length)
    return res

def part2():
    min_loc = math.inf
    for i in range(0, len(seeds), 2):
        seed_range_start = seeds[i]
        seed_range_length = seeds[i + 1]
        range_start, range_length = seed_range_start, seed_range_length
        res = process_range(maps, 0, range_start, range_length)
        min_loc = min(min_loc, min(loc_start for (loc_start, _) in res))
    return min_loc

print(f"part two :: {part2()}")
