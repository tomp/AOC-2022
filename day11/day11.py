#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 11
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
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
        """,
        10605
    ),
]

SAMPLE_CASES2 = [
    (
        """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
        """,
        2713310158
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str, strip=True) -> Lines:
    if strip:
        return [line.strip() for line in text.strip("\n").split("\n")]
    return [line for line in text.strip("\n").split("\n")]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

ADD, MUL, SQUARE = "+", "*", "^2"

@dataclass
class Operation():
    op: str
    arg: Optional[int] = None


@dataclass
class Test():
    divisor: int
    if_true: int
    if_false: int


class Monkey():
    def __init__(
        self,
        number: int,
        items: List[int],
        op: Operation,
        test: Test,
    ):
        self.number = number
        self.items = items
        self.op = op
        self.test = test
        self.inspected = 0

    @classmethod
    def from_lines(cls, lines: Lines) -> "Monkey":
        number = int(re.match(r"Monkey (\d+):$", lines[0]).group(1))
        items = list(map(int, 
                         re.match(r"Starting items: (\d[\d, ]*\d)$", lines[1])
                         .group(1).split(", ")))
        op, arg = re.match(r"Operation: new = old ([*+]) (\d+|old)$", lines[2]).groups()
        if arg == "old" and op == MUL:
            op, arg = SQUARE, None
        else:
            arg = int(arg)
        divisor = int(re.match(r"Test: divisible by (\d+)$", lines[3]).group(1))
        if_true = int(re.match(r"If true: throw to monkey (\d+)$", lines[4]).group(1))
        if_false = int(re.match(r"If false: throw to monkey (\d+)$", lines[5]).group(1))
        return cls(number, items, Operation(op, arg), Test(divisor, if_true, if_false))


class Troop():
    def __init__(self, monkeys: List[Monkey]):
        self.monkeys = monkeys
        self.modulus = math.prod(list(set([m.test.divisor for m in self.monkeys])))

    def throw_to(self, number, item):
        # print(f"--> throw item {item} to monkey {number}")
        self.monkeys[number].items.append(item)

    def turn(self, monkey: Monkey, relief: int):
        while monkey.items:
            item = monkey.items.pop(0)
            worry = item
            if monkey.op.op == ADD:
                worry = item + monkey.op.arg
            elif monkey.op.op == MUL:
                worry = item * monkey.op.arg
            elif monkey.op.op == SQUARE:
                worry = item * item
            else:
                raise RuntimeError("unsupported operation {monkey.op}")
            worry = (worry // relief ) % self.modulus
            # print(f"*** item worry level {item} -> {worry}")
            if worry % monkey.test.divisor == 0:
                self.throw_to(monkey.test.if_true, worry)
            else:
                self.throw_to(monkey.test.if_false, worry)
            monkey.inspected += 1
            
    def round(self, relief: int = 3):
        for monkey in self.monkeys:
            # print(f"Monkey {monkey.number}...")
            self.turn(monkey, relief)
        # for monkey in self.monkeys:
        #     print(f"Monkey {monkey.number}: {', '.join(map(str, monkey.items))}")

    def monkey_business(self):
        inspections = [m.inspected for m in self.monkeys]
        inspections.sort(reverse=True)
        return inspections[0] * inspections[1]

        

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    monkeys = []
    for lines in parse_sections(lines):
        monkeys.append(Monkey.from_lines(lines))
    troop = Troop(monkeys)
    for round in range(10000):
        # print(f"Round {round+1}")
        troop.round(relief=1)
    return troop.monkey_business()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    monkeys = []
    for lines in parse_sections(lines):
        monkeys.append(Monkey.from_lines(lines))
    troop = Troop(monkeys)
    for round in range(20):
        # print(f"Round {round+1}")
        troop.round()
    return troop.monkey_business()


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
    assert result == 76728
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
    assert result == 21553910156
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
