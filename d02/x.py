#!/usr/bin/env python

COLORS = {"red": 12, "blue": 14, "green": 13}
ABC = "".join(COLORS)

right = []

while True:
    inp = input()
    if inp == '':
        break
    game, data = inp.split(':')
    game = int(game.split(' ')[1])
    data = data.strip().split(';')
    is_wrong = False
    for grab in data:
        if is_wrong: break
        grab = grab.split(',')
        for cubes in grab:
            [number, color] = cubes.strip().split(' ')
            number = int(number)
            if number > COLORS[color]:
                is_wrong = True
                break
    if not is_wrong:
        right += [game]

print(f"{sum(right)}")
