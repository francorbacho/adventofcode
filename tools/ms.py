#!/usr/bin/env python
#
# bytecode interpreter that only has 5 instructions: put, mov, beq, cmp, add.

from __future__ import annotations

import re
import argparse

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
        self.ip = 0
        self._data = []

    def __setitem__(self, key, value):
        while key >= len(self._data):
            self._data.append(0)
        self._data[key] = value

    def __getitem__(self, key):
        if key >= len(self._data):
            return 0
        return self._data[key]

    def put(self, dst: Value) -> None:
        print(chr(dst.resolve(self)), end='')

    def mov(self, dst: Value, src: Value) -> None:
        src = src.resolve(self)
        dst = dst.resolve(self)
        self[dst] = src

    def add(self, dst: Value, src: Value) -> None:
        src = src.resolve(self)
        dst = dst.resolve(self)
        self[dst] += src

    def cmp(self, lhs: Value, rhs: Value) -> None:
        lhs = lhs.resolve(self)
        rhs = rhs.resolve(self)
        self.eqflag = lhs == rhs

    def beq(self, val: Value) -> None:
        if self.eqflag:
            self.ip = val.resolve(self)

    def jmp(self, val: Value) -> None:
        self.ip = val.resolve(self)

parser = argparse.ArgumentParser(
    prog='ms',
    description='bytecode interpreter',
)

parser.add_argument('filename')

args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.readlines()

skip_spaces = r'\s*'
op_re = r'put|mov|beq|cmp|add'
arg_re = r'\*?0x[0-9a-fA-F]+'

lang_regex = f'({op_re}){skip_spaces}({arg_re}){skip_spaces}({arg_re})?'

vm = VM()

for line in lines:
    line = line.split('#')[0]
    line = line.strip()
    if line == '':
        continue

    m = re.search(lang_regex, line)
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
    elif op == 'beq':
        assert arg1 is not None, 'beq with no arguments'
        assert arg2 is not None, 'beq with one argument'
        vm.beq(arg1, arg2)
    elif op == 'cmp':
        assert arg1 is not None, 'cmp with no arguments'
        assert arg2 is not None, 'cmp with one argument'
        vm.cmp(arg1, arg2)
    else:
        assert False
