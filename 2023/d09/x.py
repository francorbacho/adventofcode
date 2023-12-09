#!/usr/bin/env python

import fileinput

def diff_seq(a: list[int]) -> list[int]:
    return [a[i + 1] - a[i] for i in range(0, len(a) - 1)]

def extrapolate(a: list[int]) -> int:
    if all(node == 0 for node in a):
        return 0

    extrapolation = extrapolate(diff_seq(a))
    return a[-1] + extrapolation

def backwards_extrapolate(a: list[int]) -> int:
    if all(node == 0 for node in a):
        return 0

    extrapolation = backwards_extrapolate(diff_seq(a))
    return a[0] - extrapolation

def part1():
    res = 0
    for seq in seqs:
        res += extrapolate(seq)

    print(f"res :: {res}")

def part2():
    res = 0
    for seq in seqs:
        res += backwards_extrapolate(seq)

    print(f"res :: {res}")

lines = [line for line in fileinput.input()]
seqs = [[int(node) for node in line.split(' ')] for line in lines]

part1()
part2()
