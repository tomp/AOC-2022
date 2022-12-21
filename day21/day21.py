#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 21
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
        """,
        152
    ),
]

SAMPLE_CASES2 = [
    (
        """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
        """,
        301
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = [line for line in text.strip("\n").split("\n")]
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]


# Solution

ADD, SUB, MUL, DIV, EQ = "+", "-", "*", "/", "=="

MONKEY_RE = re.compile(r"([a-z]{4}): (\d+|[a-z]{4} [-+*/] [a-z]{4})$")

@dataclass
class Expr():
    arg1: str
    op: str
    arg2: str

    def expand(self, val1, val2):
        if isinstance(val1, int) and isinstance(val2, int):
            return self.value(val1, val2)
        return (self.op, val1, val2)

    def value(self, val1: int, val2: int) -> int:
        if self.op == ADD:
            return val1 + val2
        if self.op == SUB:
            return val1 - val2
        if self.op == MUL:
            return val1 * val2
        if self.op == DIV:
            return val1 // val2
        if self.op == EQ:
            return val1 == val2
        raise ValueError(f"unsupported operatin '{self.op}'")


class Monkey():
    def __init__(
        self, name: str,
        expr: Optional[Expr] = None,
        val: Optional[int] = None
    ):
        self.name = name
        self.expr = expr
        self.val = val

    def expand(self, apes: Dict[str, "Monkey"]):
        if self.val is None:
            return self.expr.expand(
                apes[self.expr.arg1].expand(apes),
                apes[self.expr.arg2].expand(apes)
            )
        return self.val

    def value(self, apes: Dict[str, "Monkey"]) -> int:
        if self.val is None:
            self.val = self.expr.value(
                apes[self.expr.arg1].value(apes),
                apes[self.expr.arg2].value(apes)
            )
        return self.val

@dataclass
class Troop():
    apes: Dict[str, Monkey]

    def expand(self):
          return self.apes['root'].expand(self.apes)

    def value(self):
          return self.apes['root'].value(self.apes)


def parse_lines(lines: Lines) -> Dict[str, Monkey]:
    troop = {}
    for line in lines:
        name, expr = MONKEY_RE.match(line.strip()).groups()
        if " " in expr:
            troop[name] = Monkey(name, expr=Expr(*expr.split()))
        else:
            troop[name] = Monkey(name, val=int(expr))
    return Troop(troop)

def solve_equation(eqn):
    op, arg1, arg2 = eqn
    assert op == EQ and isinstance(arg2, int)
    expr, value = arg1, arg2
    while isinstance(expr, tuple):
        op, arg1, arg2 = expr
        if isinstance(arg2, int):
            if op == ADD:
                value = int(value - arg2)
                expr = arg1
            elif op == SUB:
                value = int(value + arg2)
                expr = arg1
            elif op == MUL:
                value = int(value / arg2)
                expr = arg1
            elif op == DIV:
                value = int(value * arg2)
                expr = arg1
        elif isinstance(arg1, int):
            if op == ADD:
                value = int(value - arg1)
                expr = arg2
            elif op == SUB:
                value = int(arg1 - value)
                expr = arg2
            elif op == MUL:
                value = int(value / arg1)
                expr = arg2
            elif op == DIV:
                value = int(arg1 / value)
                expr = arg2
        else:
            break
    return (EQ, expr, value)


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    troop = parse_lines(lines)
    troop.apes["root"].expr.op = EQ
    troop.apes["humn"].val = "HUMN"

    eqn = troop.expand()
    print(eqn)
    result = solve_equation(eqn)
    print(result)

    if result[0] == EQ and result[1] == "HUMN":
        return int(result[2])
    return -1

def solve(lines: Lines) -> int:
    """Solve the problem."""
    troop = parse_lines(lines)
    return troop.value()


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 72664227897438
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 3916491093817
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
