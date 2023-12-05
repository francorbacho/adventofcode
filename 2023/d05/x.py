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
            irs = conversion.input_range_start
            l = conversion.length
            if irs <= source < irs + l:
                return conversion.output_range_start + source - irs
        return source


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
print(maps)

min_seed = math.inf
min_location = math.inf
for i, seed in enumerate(seeds):
    source = seed
    for category in maps:
        destination = category.convert(source)
        source = destination
    if min_location > source:
        min_location = source
        min_seed = seed
    print(f"seed #{i + 1} :: {seed} :: {source}")

print(f"min seed :: {min_seed} with location :: {min_location}")
