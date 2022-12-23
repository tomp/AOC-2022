#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 23
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

from pos import Pos, NORTH, SOUTH, EAST, WEST


INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
        """,
        110
    ),
]

SAMPLE_CASES2 = SAMPLE_CASES


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

EMPTY, HASH = ".", "#"


class Board():
    def __init__(self, elves: List[Pos]):
        self.elves = set(elves)
        self.steps = 0

    def bounds(self) -> Tuple[int, int, int, int]:
        return (
            min([pos.row for pos in self.elves]),
            max([pos.row for pos in self.elves]),
            min([pos.col for pos in self.elves]),
            max([pos.col for pos in self.elves]),
        )

    def display(self, title: str = ""):
        if not title:
            title = f"Step {self.steps}"
        print(f"== {title} ==")

        rowmin, rowmax, colmin, colmax = self.bounds()
        rowmin, rowmax, colmin, colmax = -2, 9, -3, 10
        for row in range(rowmin, rowmax+1):
            cells = [
                "#" if Pos(row, col) in self.elves else "."
                for col in range(colmin, colmax + 1)
            ]
            print("".join(cells))

    def empty_cells(self) -> int:
        rowmin, rowmax, colmin, colmax = self.bounds()
        area = (rowmax - rowmin + 1) * (colmax - colmin + 1)
        return area - len(self.elves)

    def single_step(self):
        next_pos: Dict[Pos, Pos] = {}
        elves = list(self.elves)
        elves.sort()

        NSWE = [NORTH, SOUTH, WEST, EAST]

        # First half of round
        proposals: Dict[Pos, int] = defaultdict(int)
        for pos in elves:
            if not any([nayb in elves for nayb in pos.neighbors()]):
                # no neighbors - do nothing
                next_pos[pos] = pos
                print(f"... elf @{pos} OK")
                continue

            move_to = pos
            for i in range(4):
                idx = (i + self.steps) % 4
                look_dir = NSWE[idx]
                if not any([nayb in elves for nayb in pos.neighbors(look_dir)]):
                    print(f"... elf @{pos} - move {look_dir}")
                    move_to = pos.direction(look_dir)
                    break
            next_pos[pos] = move_to
            proposals[move_to] += 1

        # Second half of round
        self.elves = set()
        for pos, dest in sorted(next_pos.items()):
            if dest == pos:
                self.elves.add(pos)
                print(f">>> elf @{pos} OK")
            elif proposals[dest] > 1:
                self.elves.add(pos)
                print(f">>> elf @{pos} has collision @{dest}")
            else:
                self.elves.add(dest)
                print(f">>> elf @{pos} moves to @{dest}")

        self.steps += 1

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    elves = []
    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            if cell == HASH:
                elves.append(Pos(row, col))

    board = Board(elves)
    board.display("Initially")

    for _ in range(10):
        print()
        board.single_step()
        board.display(f"End of Round {board.steps}")

    return board.empty_cells()


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
    assert result == -1
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
    assert result == -1
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
