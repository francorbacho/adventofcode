#!/usr/bin/env python

import fileinput

def diff_seq(a: list[int]) -> list[int]:
    return [a[i + 1] - a[i] for i in range(0, len(a) - 1)]

def extrapolate(a: list[int]) -> int:
    if all(node == 0 for node in a):
        return 0

    extrapolation = extrapolate(diff_seq(a))
    return a[-1] + extrapolation

lines = [line for line in fileinput.input()]
seqs = [[int(node) for node in line.split(' ')] for line in lines]

def part1():
    res = 0
    for seq in seqs:
        res += extrapolate(seq)

    print(f"res :: {res}")

part1()
