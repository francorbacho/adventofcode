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

    # returns true if it can emit at least one value of the output range provided
    def can_emit_output_range(self, wanted_range_start: int, length: int) -> bool:
        if self.output_range_start <= wanted_range_start < self.output_range_start + self.length:
            return True
        return wanted_range_start <= self.output_range_start <= wanted_range_start + length

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

    def min_output_range(self) -> int:
        mor = math.inf
        mori = math.inf
        for i, conversion in enumerate(self.conversions):
            if mor > conversion.output_range_start:
                mor = conversion.output_range_start
                mori = i
        return self.conversions[mori]

    def who_maps_to_output_range(self, output_range_start: int, length: int) -> list[Conversion]:
        result = []
        for conversion in self.conversions:
            if conversion.can_emit_output_range(output_range_start, length):
                result.append(conversion)
        return result

    def smallest_unmapped_input(self) -> int:
        small = 0
        i = 0
        while i < len(self.conversions):
            conv = self.conversions[i]
            if conv.input_range_start <= small < conv.input_range_start + conv.length:
                small = conv.input_range_start + conv.length
                i = 0
                continue
            i += 1
        return small

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

min_seed = math.inf
min_location = math.inf
for i, seed in enumerate(seeds):
    destination = process_seed(seed)
    if min_location > destination:
        min_location = destination
        min_seed = seed
    print(f"seed #{i + 1} :: {seed} :: {destination}")

print(f"min seed :: {min_seed} with location :: {min_location}")

def process_range(maps: list[Map], imap: int, range_start: int, range_length: int) -> list[tuple[int, int]]:
    if imap == len(maps) - 1:
        return maps[imap].convert_range(range_start, range_length)
    res = []
    for (new_range_start, new_range_length) in maps[imap].convert_range(range_start, range_length):
        res += process_range(maps, imap + 1, new_range_start, new_range_length)
    return res

min_loc = math.inf
for i in range(0, len(seeds), 2):
    seed_range_start = seeds[i]
    seed_range_length = seeds[i + 1]
    range_start, range_length = seed_range_start, seed_range_length
    res = process_range(maps, 0, range_start, range_length)
    min_loc = min(min_loc, min(loc_start for (loc_start, _) in res))

print(f"result is :: {min_loc}")
