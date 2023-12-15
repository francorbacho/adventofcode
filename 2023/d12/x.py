#!/usr/bin/env python

import fileinput

lines = [line.strip() for line in fileinput.input() if line.strip() != ""]

def matches(row: str, groups: list[int]) -> bool:
    assert '?' not in row
    actual_groups = [len(g) for g in row.split('.') if g != '']
    return actual_groups == groups

def count_arrangements(row: str, groups: list[int]) -> None:
    if "?" not in row:
        return 1 if matches(row, groups) else 0
    lhs = count_arrangements(row.replace("?", "#", 1), groups)
    rhs = count_arrangements(row.replace("?", ".", 1), groups)
    return lhs + rhs

def part1(lines: list[str]) -> None:
    springs, groups = [], []
    for l in lines:
        [row_springs, row_groups] = l.split(' ')
        row_groups = [int(num) for num in row_groups.split(',')]
        springs.append(row_springs)
        groups.append(row_groups)
    return sum(count_arrangements(*s) for s in zip(springs, groups, strict=True))

print(f"part1 :: {part1(lines)}")
