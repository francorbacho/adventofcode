#!/usr/bin/env python

with open("input.txt", "r") as f:
    lines = f.readlines()

numbers = [list(filter(lambda x: ord('0') <= ord(x) <= ord('9'), line)) for line in lines]
numbers = [int(''.join(number[:1] + number[-1:])) for number in numbers]
result = sum(numbers)

print(result)
