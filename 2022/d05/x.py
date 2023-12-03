#!/usr/bin/python

import re
import sys

def parse_state(lines: list[str]):
    # Remove column numbers
    lines = lines[:-1]

    # [A] -> A
    PATTERN = "[\[\]]"
    REPL = " "
    lines = [re.sub(PATTERN, REPL, line) for line in lines]

    # "  " -> " "
    PATTERN = "   "
    REPL = " "
    lines = [re.sub(PATTERN, REPL, line) for line in lines]

    lines = [line for line in lines[::-1]]
    lines = "\n".join(lines)

    PATTERN = "\n\n"
    REPL = "\n"
    lines = re.sub(PATTERN, REPL, lines)
    lines = lines.split('\n')
    lines = [line.lstrip() for line in lines]

    state = [list(' ' * 8) for i in range(9)]

    _lines = ["".join(stack) for stack in lines]

    # for _line in _lines: print("'" + _line + "'")

    try:
        for i in range(len(state)):
            j = 0
            for line in lines:
                crate = line[i * 2]
                state[i][j] = crate
                j += 1
    except IndexError:
        pass

    for i, stack in enumerate(state):
        state[i] = [crate for crate in stack if crate.strip() != '']

    return state

def parse_cmd(line: str):
    PATTERN = r"\d+"
    match = re.findall(PATTERN, line)
    [rep, src, dest] = list(map(int, match))
    src -= 1
    dest -= 1
    return rep, src, dest

if '-2' not in sys.argv:
    def apply_cmd(state: list[list[str]], cmd: tuple[int, int, int]):
        (rep, src, dest) = cmd
        for _ in range(rep):
            state[dest].append(state[src].pop())
        return state
else:
    def apply_cmd(state: list[list[str]], cmd: tuple[int, int, int]):
        (rep, src, dest) = cmd
        crates = state[src][-rep:]
        state[src] = state[src][:-rep]
        state[dest].extend(crates)
        return state

def print_state(state: list[list[str]]):
    print('------------')
    _state = ["".join(crate) for crate in state]
    _state = ["'" + line.strip() + "'" for line in _state]
    for crate in _state: print(crate)
    print('------------')

def main():
    with open("input-state.txt", "r") as f:
        state = f.readlines()
        state = [line.strip("\n") for line in state]
        state = parse_state(state)

    with open("input-cmds.txt", "r") as f:
        cmds = f.readlines()
        cmds = [parse_cmd(line) for line in cmds]

    # _state = ["".join(crate) for crate in state]
    # _state = ["'" + line.strip() + "'" for line in _state]
    # for crate in _state: print(crate)

    for cmd in cmds:
        state = apply_cmd(state, cmd)

    _state = [crate[-1] for crate in state]
    _state = "".join(_state)
    print(_state)

if __name__ == "__main__":
    main()
