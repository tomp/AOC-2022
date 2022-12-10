#!/usr/bin/env python3
from typing import Sequence, Union, Optional, Any, List, Dict
from dataclasses import dataclass


Lines = Sequence[str]

Opcode = str

OPCODE: Dict[Opcode, int] = {
    "addx": 2,
    "noop": 1,
}

LIT, DARK = "#", "."


@dataclass
class Instruction():
    """A single instruction for the computing device."""
    op: Opcode
    val: int = 0


class Device():
    """A computing device with four numeric registers and 16 instructions."""
    NROW = 6
    NCOL = 40

    def __init__(
        self,
        prog: Optional[list[Instruction]] = None,
        reg: list[int] = [1]
    ):
        self.prog = []
        if prog:
            self.prog = list(prog)
        self.reg = list(reg)
        self._reset()

        self.clock = 0
        self.pc = 0
        self.history = [self.reg[0]]
        self._executing = 0

    def load_prog(self, lines: Lines) -> "Device":
        self.prog = []
        for line in lines:
            line = line.replace(",", " ")
            fields = line.split()
            if len(fields) == 1:
                self.prog.append(Instruction(fields[0]))
            elif len(fields) == 2:
                self.prog.append(Instruction(fields[0], int(fields[1])))
            else:
                raise ValueError(f"unparseable instruction '{line}'")

    def _reset(self) -> "Device":
        self.pc = 0
        self.clock = 0
        self._executing = 0
        self.pixels = [' '] * self.NROW * self.NCOL
        self.history = [self.reg[0]]
        return self

    def display(self):
        for row in range(self.NROW):
            print("".join(self.pixels[row * self.NCOL:(row+1) * self.NCOL]))

    def run(self):
        while 0 <= self.pc < len(self.prog):
            self.step()
            # print(f"after cycle {self.clock:3d},  pc:{self.pc:3d}  X: {self.reg[0]}")
            # print(f"during cycle {self.clock:3d},  X: {self.history[-1]}")
        self.history.append(self.reg[0])

    def step(self):
        """Excute a single instruction."""
        self.clock += 1
        self.history.append(self.reg[0])

        pixel = (self.clock - 1) % self.NCOL
        if self.reg[0] - 1 <= pixel <= self.reg[0] + 1:
            self.pixels[self.clock - 1] = LIT
        else:
            self.pixels[self.clock - 1] = DARK

        ins = self.prog[self.pc]
        if ins.op == "noop":
            self.pc += 1
        elif ins.op == "addx":
            if self._executing:
                self._executing -= 1
                if not self._executing:
                    self.reg[0] += ins.val
                    self.pc += 1
            else:
                self._executing = OPCODE[ins.op] - 1


