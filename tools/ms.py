#!/usr/bin/env python
#
# bytecode interpreter that only has 8 instructions: put, mov, beq, blt, cmp,
# add, sub, jmp, hlt.

from __future__ import annotations

import argparse
import re
import sys

class Value:
    def __init__(self, value: int, *, is_ptr = False) -> None:
        self.value = value
        self.is_ptr = is_ptr

    def from_str(arg: str):
        assert arg is not None
        if arg[0] == '*':
            return Value(int(arg[1:], base=16), is_ptr=True)
        return Value(int(arg, base=16))

    def resolve(self, vm: VM) -> int:
        return vm[self.value] if self.is_ptr else self.value

class VM:
    def __init__(self):
        self.eqflag = False
        self.ltflag = False
        self.ip = 0
        self._data = []

    def __setitem__(self, key, value):
        assert key >= 0
        while key >= len(self._data):
            self._data.append(0)
        self._data[key] = value

    def __getitem__(self, key):
        assert key >= 0
        if key >= len(self._data):
            return 0
        return self._data[key]

    def put(self, dst: Value) -> None:
        print(chr(dst.resolve(self)), flush=True, end='')

    def mov(self, dst: Value, src: Value) -> None:
        src = src.resolve(self)
        dst = dst.resolve(self)
        self[dst] = src

    def add(self, dst: Value, src: Value) -> None:
        src = src.resolve(self)
        dst = dst.resolve(self)
        self[dst] += src

    def sub(self, dst: Value, src: Value) -> None:
        src = src.resolve(self)
        dst = dst.resolve(self)
        self[dst] -= src

    def cmp(self, lhs: Value, rhs: Value) -> None:
        lhs = lhs.resolve(self)
        rhs = rhs.resolve(self)
        self.eqflag = lhs == rhs
        self.ltflag = lhs < rhs

    def blt(self, val: Value) -> None:
        if self.ltflag:
            self.ip = val.resolve(self)

    def beq(self, val: Value) -> None:
        if self.eqflag:
            self.ip = val.resolve(self)

    def jmp(self, val: Value) -> None:
        self.ip = val.resolve(self)


def run(vm: VM, lines: list[str]):
    skip_spaces = r'\s*'
    op_re = r'put|mov|beq|blt|cmp|add|sub|jmp|hlt'
    arg_re = r'\*?0x[0-9a-fA-F]+'

    lang_regex = f'({op_re}){skip_spaces}({arg_re})?{skip_spaces}({arg_re})?'

    while vm.ip < len(lines):
        line = lines[vm.ip]
        vm.ip += 1

        line = line.split('#')[0]
        if line == '':
            continue

        m = re.search(lang_regex, line)
        if m is None:
            print(f'could not parse line: "{line}"', file=sys.stderr)
            sys.exit(1)

        op = m.group(1)
        arg1 = m.group(2)
        arg2 = m.group(3)

        arg1 = None if arg1 is None else Value.from_str(arg1)
        arg2 = None if arg2 is None else Value.from_str(arg2)

        if op == 'put':
            assert arg1 is not None, 'put with no arguments'
            assert arg2 is None, 'put with more than one argument'
            vm.put(arg1)
        elif op == 'mov':
            assert arg1 is not None, 'mov with no arguments'
            assert arg2 is not None, 'mov with one argument'
            vm.mov(arg1, arg2)
        elif op == 'add':
            assert arg1 is not None, 'add with no arguments'
            assert arg2 is not None, 'add with one argument'
            vm.add(arg1, arg2)
        elif op == 'sub':
            assert arg1 is not None, 'sub with no arguments'
            assert arg2 is not None, 'sub with one argument'
            vm.sub(arg1, arg2)
        elif op == 'beq':
            assert arg1 is not None, 'beq with no arguments'
            assert arg2 is not None, 'beq with one argument'
            vm.beq(arg1, arg2)
        elif op == 'blt':
            assert arg1 is not None, 'blt with no arguments'
            assert arg2 is None, 'blt with two arguments'
            vm.blt(arg1)
        elif op == 'cmp':
            assert arg1 is not None, 'cmp with no arguments'
            assert arg2 is not None, 'cmp with one argument'
            vm.cmp(arg1, arg2)
        elif op == 'jmp':
            assert arg1 is not None, 'jmp with no arguments'
            assert arg2 is None, 'jmp with two arguments'
            vm.jmp(arg1)
        elif op == 'hlt':
            assert arg1 is None, 'hlt with arguments'
            assert arg2 is None, 'hlt with arguments'
            break
        else:
            assert False

def main():
    parser = argparse.ArgumentParser(
        prog='ms',
        description='bytecode interpreter',
    )

    parser.add_argument('filename')

    args = parser.parse_args()

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    vm = VM()
    try:
        run(vm, lines)
    except KeyboardInterrupt:
        print(f"keyboard interrupt on line {vm.ip}: '{lines[vm.ip]}'", file=sys.stderr)

if __name__ == '__main__':
    main()
