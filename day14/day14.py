#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 14
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
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
        """,
        24
    ),
]

SAMPLE_CASES2 = [
    (
        """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
        """,
        93
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

EMPTY, SAND, ROCK , SOURCE, FLOW = ".", "o", "#", "+", "~"
ARROW = " -> "

@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    @classmethod
    def parse_xy(cls, text) -> "Pos":
        x, y = text.split(",")
        row, col = int(y.strip()), int(x.strip())
        return cls(row, col)

    def path_to(self, other: "Pos") -> "List[Pos]":
        if other == self:
            return [self]
        if other.row == self.row:
            step = -1 if other.col < self.col else 1
            return [Pos(self.row, col) for col in range(self.col, other.col + step, step)]
        step = -1 if other.row < self.row else 1
        return [Pos(row, self.col) for row in range(self.row, other.row + step, step)]

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col),
        ]

    def paths_down(self) -> "List[Pos]":
        return [
            Pos(self.row + 1, self.col),
            Pos(self.row + 1, self.col - 1),
            Pos(self.row + 1, self.col + 1),
        ]

    def above(self) -> "Pos":
        return Pos(self.row - 1, self.col)

    def below(self) -> "Pos":
        return Pos(self.row + 1, self.col)

    def right(self) -> "Pos":
        return Pos(self.row, self.col + 1)

    def left(self) -> "Pos":
        return Pos(self.row, self.col - 1)


Cell = str


class Board():
    grid: dict[Pos, Cell]

    def __init__(self, cells, floor=False):
        self.grid = cells
        self.rowmax = max([v.row for v in self.grid.keys()])
        self.rowmin = min([v.row for v in self.grid.keys()])
        self.colmax = max([v.col for v in self.grid.keys()])
        self.colmin = min([v.col for v in self.grid.keys()])

        if floor:
            self.floor = self.rowmax + 2
            self.rowmax = self.floor - 1
        else:
            self.floor = 0

        self.flow = []
        for pos, cell in self.grid.items():
            if cell == SOURCE:
                self.flow.append(pos)

    @classmethod
    def from_lines(cls, lines, **kwargs) -> "Board":
        grid = defaultdict(lambda : EMPTY)
        grid[Pos(0, 500)] = SOURCE
        for line in lines:
            points = line.split(ARROW)
            start = Pos.parse_xy(points[0])
            for point in points[1:]:
                end = Pos.parse_xy(point)
                for pos in start.path_to(end):
                    grid[pos] = ROCK
                start = end
        return cls(grid, **kwargs)

    def print(self, title="", overlay=None):
        if title:
            print(title)
        for r in range(self.rowmin, self.rowmax+1):
            row = []
            for c in range(self.colmin-1, self.colmax+2):
                pos = Pos(r, c)
                val = self.grid[pos][0]
                if overlay and pos in overlay:
                    val = overlay[pos]
                row.append(val)
            print("".join(row))

        if self.floor:
            row = []
            for c in range(self.colmin-1, self.colmax+2):
                pos = Pos(self.floor, c)
                row.append(ROCK)
            print("".join(row))

    def count_sand(self) -> int:
        return len([pos for pos, cell in self.grid.items() if cell == SAND])

    def step(self) -> bool:
        """Propagate the system for one time step.  Return True if the
        sand is now flowing into the abyss.
        """
        while self.flow:
            pos = self.flow[-1]
            if not self.floor or pos.row < self.floor - 1:
                for next_pos in pos.paths_down():
                    if self.grid[next_pos] == EMPTY:
                        self.grid[next_pos] = FLOW
                        self.flow.append(next_pos)
                        if next_pos.row < max(self.rowmax, self.floor):
                            return False
                        return True

            self.grid[pos] = SAND
            self.flow.pop()
        return True

    def run(self, max_steps: int = 0) -> int:
        """Propagate the system until it reaches steady state, or the max_steps have
        been exceeded.  The number of steps taken is returned.
        """
        done = False
        steps = 0
        while not done:
            steps += 1
            if max_steps and steps > max_steps:
                break 
            # print(f"--- step {steps}")
            done = self.step()
            # self.print(title=f"Step {steps}:")
        return steps


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines, floor=True)
    board.print(title="Initially:")
    board.run()
    board.print(title="Final:")
    return board.count_sand()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    board.print(title="Initially:")
    board.run()
    board.print(title="Final:")
    return board.count_sand()


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
    assert result == 665
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
    assert result == 25434
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
