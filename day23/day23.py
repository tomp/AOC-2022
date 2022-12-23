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

from pos import Pos, NORTH, SOUTH, EAST, WEST, neighbors, direction


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

SAMPLE_CASES2 = [
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
        20
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

EMPTY, HASH = ".", "#"


class Board():
    def __init__(self, elves: List[Pos]):
        self.elves = elves
        self.steps = 0

        self.elves.sort()

    def bounds(self) -> Tuple[int, int, int, int]:
        return (
            min([pos[0] for pos in self.elves]),
            max([pos[0] for pos in self.elves]),
            min([pos[1] for pos in self.elves]),
            max([pos[1] for pos in self.elves]),
        )

    def display(self, title: str = ""):
        if not title:
            title = f"Step {self.steps}"
        print(f"== {title} ==")

        rowmin, rowmax, colmin, colmax = self.bounds()
        for row in range(rowmin-2, rowmax+3):
            cells = [
                "#" if (row, col) in self.elves else "."
                for col in range(colmin-2, colmax+3)
            ]
            print("".join(cells))

    def empty_cells(self) -> int:
        rowmin, rowmax, colmin, colmax = self.bounds()
        area = (rowmax - rowmin + 1) * (colmax - colmin + 1)
        return area - len(self.elves)

    def single_step(self):
        next_pos: List[Pos, Pos] = []
        elves = self.elves # just an alias, to keep code more compact
        elf_positions = set(self.elves)

        NSWE = [NORTH, SOUTH, WEST, EAST]

        # First half of round
        proposals: Dict[Pos, int] = defaultdict(int)
        for pos in elves:
            move_to = pos
            for nayb in neighbors(pos):
                if nayb in elf_positions:
                    move_to = None
                    break
            if move_to == pos:
                next_pos.append((pos, pos))
                # print(f"... elf @{pos} OK")
                continue

            for i in range(4):
                idx = (i + self.steps) % 4
                look_dir = NSWE[idx]
                block = None
                for nayb in neighbors(pos, look_dir):
                    if nayb in elf_positions:
                        block = nayb
                        break
                if block is None:
                    move_to = direction(pos, look_dir)
                    # print(f"... elf @{pos} - move {look_dir}")
                    break

            if move_to is not None:
                next_pos.append((pos, move_to))
                proposals[move_to] += 1
            else:
                next_pos.append((pos, pos))

        # Second half of round
        self.elves = []
        moved = 0
        for pos, dest in next_pos:
            if dest == pos:
                self.elves.append(pos)
                # print(f">>> elf @{pos} OK")
            elif proposals[dest] > 1:
                self.elves.append(pos)
                # print(f">>> elf @{pos} has collision @{dest}")
            else:
                self.elves.append(dest)
                moved += 1
                # print(f">>> elf @{pos} moves to @{dest}")

        self.steps += 1
        return moved == 0

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    elves = []
    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            if cell == HASH:
                elves.append((row, col))

    board = Board(elves)
    # if len(elves) < 40:
    #     board.display("Initially")

    done = False
    while not done:
        done = board.single_step()
        # if len(elves) < 40:
        #     print()
        #    board.display(f"End of Round {board.steps}")

    return board.steps

def solve(lines: Lines) -> int:
    """Solve the problem."""
    elves = []
    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            if cell == HASH:
                elves.append((row, col))

    board = Board(elves)
    # if len(elves) < 40:
    #     board.display("Initially")

    for _ in range(10):
        board.single_step()
        # if len(elves) < 40:
        #     print()
        #     board.display(f"End of Round {board.steps}")

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
    assert result == 3762
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
    assert result == 997
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
