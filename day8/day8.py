#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 8
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
30373
25512
65332
33549
35390
        """,
        21
    ),
]

SAMPLE_CASES2 = [
    (
        """
30373
25512
65332
33549
35390
        """,
        8
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

def visible_trees(lines) -> int:
    visible = set()

    nrow, ncol = len(lines), len(lines[0])

    # count from left
    for row in range(nrow):
        highest = -1
        for col in range(ncol):
            # print(f"({row}, {col})")
            height = int(lines[row][col])
            # print(f"({row}, {col}) height {height}")
            if height > highest:
                # print(f"({row}, {col}) height {height} VISIBLE")
                visible.add((row, col))
                highest = height

    # count from right
    for row in range(nrow):
        highest = -1
        for col in range(ncol-1, -1, -1):
            height = int(lines[row][col])
            if height > highest:
                visible.add((row, col))
                highest = height

    # count from top
    for col in range(ncol):
        highest = -1
        for row in range(nrow):
            height = int(lines[row][col])
            if height > highest:
                visible.add((row, col))
                highest = height

    # count from bottom
    for col in range(ncol):
        highest = -1
        for row in range(nrow-1, -1, -1):
            height = int(lines[row][col])
            if height > highest:
                visible.add((row, col))
                highest = height

    return visible


def scenic_score(grid, pos) -> int:
    r, c = pos
    nrow, ncol = len(grid), len(grid[0])
    assert (-1 < r < nrow) and (-1 < c < ncol)

    if r == 0 or r == nrow-1 or c == 0 or c == ncol-1:
        return 0
                                
    up, down, right, left = 0, 0, 0, 0
    height = grid[r][c]

    for row in range(r-1, -1, -1):
        up += 1
        if grid[row][c] >= height:
              break

    for row in range(r+1, nrow):
        down += 1
        if grid[row][c] >= height:
              break

    for col in range(c+1, ncol):
        right += 1
        if grid[r][col] >= height:
              break

    for col in range(c-1, -1, -1):
        left += 1
        if grid[r][col] >= height:
              break

    score = up * left  * down * right
    # print(f"({r}, {c}) height {height}  visible: {up}, {left}, {down}, {right} --> score {score}")

    return score


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    grid = [[int(height) for height in row] for row in lines]
    nrow, ncol = len(grid), len(grid[0])
    best = 0
    for row in range(nrow):
        for col in range(ncol):
            score = scenic_score(grid, (row, col))
            if score > best:
                best = score
    return best

def solve(lines: Lines) -> int:
    """Solve the problem."""
    visible = visible_trees(lines)
    return len(visible)


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
    assert result == 1669
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
    assert result == 331344
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
