#!/usr/bin/env python

from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import threading
from functools import cache

import fileinput
import sys

@cache
def matches(row: str, groups: list[int]) -> bool:
    assert '?' not in row
    actual_groups = [len(g) for g in row.split('.') if g != '']
    return actual_groups == groups

@cache
def is_broken(row_: str, groups: list[int]) -> bool:
    # print(f"is {row_} broken ??  ", end="")
    if '?' not in row_:
        # print("matcher")
        return not matches(row_, groups)
    qmark_i = row_.find("?")
    if qmark_i > 0:
        actual_groups = [len(g) for g in row_[:qmark_i].split('.') if g != ""]
        if any([a[0] > a[1] for a in zip(actual_groups, groups)]):
            # print("quicky true")
            return True

        if row_[qmark_i - 1] != '.':
            # print("quicky false")
            return False

    row = row_[:qmark_i]
    actual_groups = [len(g) for g in row.split('.') if g != '']
    r= actual_groups != groups[:len(actual_groups)]
    # print(r)
    return r

def count_arrangements(row: str, groups: list[int]) -> None:
    if "?" not in row:
        return 1 if matches(row, groups) else 0
    lhs_s = row.replace("?", "#", 1)
    lhs = 0 if is_broken(lhs_s, groups) else count_arrangements(lhs_s, groups)

    rhs_s = row.replace("?", ".", 1)
    rhs = 0 if is_broken(rhs_s, groups) else count_arrangements(rhs_s, groups)
    return lhs + rhs

def part1(lines: list[str]) -> None:
    springs, groups = [], []
    for l in lines:
        [row_springs, row_groups] = l.split(' ')
        row_groups = [int(num) for num in row_groups.split(',')]
        springs.append(row_springs)
        groups.append(row_groups)
    return sum(count_arrangements(*s) for s in zip(springs, groups, strict=True))

def part2(lines: list[str]) -> None:
    springs, groups = [], []
    for l in lines:
        [row_springs, row_groups] = l.split(' ')
        row_groups = [int(num) for num in row_groups.split(',')]
        # unfold
        row_springs = "?".join([row_springs] * 5)
        row_groups = row_groups * 5

        springs.append(row_springs)
        groups.append(row_groups)

    def pline(s):
        try:
            r = count_arrangements(*s)
        except:
            print("something went wrong :(")
            return 0
        print(f"{threading.current_thread().name} :: {r}")
        return r

    pool = ThreadPool(cpu_count())
    results = pool.map(pline, list(zip(springs, groups, strict=True)))
    return sum(results)

# s, g = "??.?#??##??.##?##.?", [7,5]
# # s, g = ".??..??...?##.", [1,1,3]
# s, g = "??????#????????", [7,2]
#
#
# print("?".join([s] * 5))
# print(g * 5)
#
# print("r:", count_arrangements(s, g))
# print("r:", count_arrangements("?".join([s] * 5), g * 5))

if not sys.flags.interactive:
    lines = [line.strip() for line in fileinput.input() if line.strip() != ""]

    print(f"part1 :: {part1(lines)}")
    print(f"part2 :: {part2(lines)}")

