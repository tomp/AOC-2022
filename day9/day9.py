#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 9
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
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
        """,
        13
    ),
]

SAMPLE_CASES2 = [
    (
        """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
        """,
        1
    ),
    (
        """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
        """,
        36
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> Tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

HEAD, TAIL = "H", "T"
DIRS = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}


@dataclass(order=True, frozen=True)
class Delta():
    dr: int
    dc: int

    def __str__(self) -> str:
        return f"d({self.dr},{self.dc})"

    def __add__(self, other: Union["Pos", "Delta"]) -> Union["Pos", "Delta"]:
        if isinstance(other, Delta): 
            return Delta(self.dr + other.dr, self.dc + other.dc)
        elif isinstance(other, Pos): 
            return Pos(self.dr + other.row, self.dc + other.col)
        raise ValueError(f"Cannot add '{type(other)}' to Delta")

    def __sub__(self, other: "Delta") -> "Delta":
        if isinstance(other, Delta): 
            return Delta(self.dr - other.dr, self.dc - other.dc)
        raise ValueError(f"Cannot subtract '{type(other)}' from Delta")

    def unit(self) -> "Delta":
        dr = self.dr // abs(self.dr) if self.dr else 0
        dc = self.dc // abs(self.dc) if self.dc else 0
        return Delta(dr, dc)

    @classmethod
    def from_dir_dist(cls, dir: str, dist: int) -> "Delta":
        dr, dc = DIRS[dir]
        return cls(dr * dist, dc * dist)


@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def is_adjacent(self, other) -> bool:
        diff = other - self
        return max(abs(diff.dr), abs(diff.dc)) < 2

    def __sub__(self, other: Union["Pos", "Delta"]) -> Union["Pos", "Delta"]:
        if isinstance(other, Delta): 
            return Pos(self.row - other.dr, self.col - other.dc)
        elif isinstance(other, Pos): 
            return Delta(self.row - other.row, self.col - other.col)
        raise ValueError(f"Cannot subtract '{type(other)}' from Pos")

    def __add__(self, other: "Delta") -> "Pos":
        if isinstance(other, Delta): 
            return Pos(self.row + other.dr, self.col + other.dc)
        raise ValueError(f"Cannot add '{type(other)}' to Pos")


class Rope():
    def __init__(self, length: int = 2):
        self.rope = [Pos(0,0)] * length

    @property
    def head(self) -> Pos:
        return self.rope[0]

    @property
    def tail(self) -> Pos:
        return self.rope[-1]

    @property
    def size(self) -> int:
        return len(self.rope)
            
    def step(self, head_step):
        self.rope[0] += head_step
        for i in range(1, len(self.rope)):
            if not self.rope[i-1].is_adjacent(self.rope[i]):
                self.rope[i] += (self.rope[i-1] - self.rope[i]).unit()

    def print(self, title: str = ""):
        rmin = min([node.row for node in self.rope])
        rmax = max([node.row for node in self.rope])
        cmin = min([node.col for node in self.rope])
        cmax = max([node.col for node in self.rope])
        nrow = rmax - rmin + 1
        ncol = cmax - cmin + 1
        grid = [["."] * ncol for _ in range(nrow)]
        for i in range(len(self.rope)-1, 0, -1):
            grid[self.rope[i].row - rmin][self.rope[i].col - cmin] = str(i)
        grid[self.rope[0].row - rmin][self.rope[0].col - cmin] = HEAD

        if title:
            print(title)
        for line in grid:
            print("".join(line))


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    LENGTH = 10
    rope = Rope(LENGTH)

    visited = set()
    visited.add(rope.tail)

    # print(f"head: {rope.head}  tail: {rope.tail}")
    for line in lines:
        heading, dist = line.split()
        head_step = Delta.from_dir_dist(heading, 1)
        for _ in range(int(dist)):
            rope.step(head_step)
            visited.add(rope.tail)
            # rope.print(title=f"head: {rope.head}  tail: {rope.tail}")

    return len(visited)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    head = Pos(0, 0)
    tail = Pos(0, 0)

    visited = set()
    visited.add(tail)

    # print(f"head: {head}  tail: {tail}")
    for line in lines:
        heading, dist = line.split()
        head_step = Delta.from_dir_dist(heading, 1)
        for _ in range(int(dist)):
            head += head_step
            if not head.is_adjacent(tail):
                tail += (head - tail).unit()
                visited.add(tail)
            # print(f"head: {head}  tail: {tail}")

    return len(visited)


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
    assert result == 2658
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
