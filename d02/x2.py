#!/usr/bin/env python

import math

powers = []

while True:
    inp = input()
    if inp == '':
        break
    game, data = inp.split(':')
    game = int(game.split(' ')[1])
    data = data.strip().split(';')
    min_red = 0
    min_green = 0
    min_blue = 0
    for grab in data:
        grab = grab.split(',')
        for cubes in grab:
            [number, color] = cubes.strip().split(' ')
            number = int(number)
            if color == "red":
                min_red = max(min_red, number)
            elif color == "green":
                min_green = max(min_green, number)
            elif color == "blue":
                min_blue = max(min_blue, number)
            else:
                assert False, color
    powers += [min_red * min_green * min_blue]

print(f"{sum(powers)}")
