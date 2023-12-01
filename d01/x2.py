#!/usr/bin/env python

numbers = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
}

def extract_numbers(line):
    firsti, lasti = len(line), -1
    first, last = None, None
    for k in numbers.keys():
        i = line.find(k)
        r = line.rfind(k)
        if i != -1 and i < firsti:
            firsti = i
            first = k
        if r != -1 and lasti < r:
            lasti = r
            last = k
    if first is None or last is None:
        raise Exception(f"error with: '{line}'; {first}, {last}")
    ret = [numbers[first], numbers[last]]
    print(f"{line.rstrip()} :: {ret}")
    return ret

with open("input.txt", "r") as f:
    lines = f.readlines()

numbers = [extract_numbers(line) for line in lines]
numbers = [int(''.join(number[:1] + number[-1:])) for number in numbers]
result = sum(numbers)

print(result)
