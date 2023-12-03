import sys

GRID_SIZE = 1200

SAND_SPAWN_X = 500
SAND_SPAWN_Y = 0

class SandOutofBounds(Exception):
    pass

class SandSpawnBlocked(Exception):
    pass

def dump_grid(file, grid):
    # for row in grid:
    #     file.write(''.join(row))
    #     file.write('\n')

    # return

    colors = {
        '.': '255 255 255\n',
        '#': '0 0 255\n',
        'o': '255 215 0\n',
        '+': '255 0 0\n',
    }

    file.write(f'P3\n')
    file.write(f'{GRID_SIZE} {GRID_SIZE}\n')
    file.write(f'255\n')

    for row in grid:
        for unit in row:
            file.write(colors[unit])

def parse_line(line):
    xys = line.split(" -> ")
    xys = [tuple(map(lambda s: int(s.strip()), xy.split(','))) for xy in xys]

    return xys

def build_grid(grid, lines, *, floor_level):
    for xys in lines:
        # xys = [(0, 1), (1, 2), (3, 2)]
        for i in range(len(xys) - 1):
            startx = xys[i][0]
            starty = xys[i][1]
            endx = xys[i + 1][0]
            endy = xys[i + 1][1]

            if startx > endx:
                startx, endx = endx, startx
            if starty > endy:
                starty, endy = endy, starty

            if startx == endx:
                x = startx
                for y in range(starty, endy + 1):
                    grid[y][x] = '#'
            if starty == endy:
                y = starty
                for x in range(startx, endx + 1):
                    grid[y][x] = '#'

    for x in range(GRID_SIZE):
        assert grid[floor_level][x] == '.'
        grid[floor_level][x] = '#'

def spawn_sand(grid):
    sand_x = SAND_SPAWN_X
    sand_y = SAND_SPAWN_Y

    while True:
        assert 0 < sand_x < GRID_SIZE
        assert 0 <= sand_y < GRID_SIZE

        if sand_y + 1 == GRID_SIZE:
            raise SandOutofBounds()

        if grid[sand_y + 1][sand_x] == '.':
            sand_y += 1
            continue
        if grid[sand_y + 1][sand_x - 1] == '.':
            sand_x -= 1
            sand_y += 1
            continue
        if grid[sand_y + 1][sand_x + 1] == '.':
            sand_x += 1
            sand_y += 1
            continue
        break

    if grid[sand_y][sand_x] == '+':
        raise SandSpawnBlocked()

    assert grid[sand_y][sand_x] != 'o'
    grid[sand_y][sand_x] = 'o'

    return sand_x, sand_y

def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    lines = [parse_line(line) for line in lines]

    max_y = 0
    for xys in lines:
        for xy in xys:
            if max_y < xy[1]:
                max_y = xy[1]

    grid = [['.' for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    grid[SAND_SPAWN_Y][SAND_SPAWN_X] = '+'

    build_grid(grid, lines, floor_level=max_y + 2)

    sand_count = 0

    try:
        while True:
            spawn_sand(grid)
            sand_count += 1
    except SandOutofBounds:
        print('sand fell out of bounds, total amount: ', sand_count)
    except SandSpawnBlocked:
        # the one in the spawner was not counted
        sand_count += 1
        print('sand spawn blocked, total amount: ', sand_count)

    with open('img.ppm', 'w+') as f:
        dump_grid(f, grid)

main()
