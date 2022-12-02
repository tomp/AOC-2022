#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 2
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
A Y
B X
C Z
        """,
        15
    ),
]

SAMPLE_CASES2 = [
    (
        """
A Y
B X
C Z
        """,
        12
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

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

WIN, DRAW, LOSS = 6, 3, 0
ROCK, PAPER, SCISSORS = 1, 2, 3

ROUND_SCORE = {
    "A X": ROCK + DRAW,
    "A Y": PAPER + WIN,
    "A Z": SCISSORS + LOSS,
    "B X": ROCK + LOSS,
    "B Y": PAPER + DRAW,
    "B Z": SCISSORS + WIN,
    "C X": ROCK + WIN,
    "C Y": PAPER + LOSS,
    "C Z": SCISSORS + DRAW,
}

RESULT_SCORE = {
    "A X": LOSS + SCISSORS,
    "A Y": DRAW + ROCK,
    "A Z": WIN  + PAPER,
    "B X": LOSS + ROCK,
    "B Y": DRAW + PAPER,
    "B Z": WIN  + SCISSORS,
    "C X": LOSS + PAPER,
    "C Y": DRAW + SCISSORS,
    "C Z": WIN  + ROCK,
}


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    score = 0
    for line in lines:
        score += RESULT_SCORE[line]
    return score

def solve(lines: Lines) -> int:
    """Solve the problem."""
    score = 0
    for line in lines:
        score += ROUND_SCORE[line]
    return score


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
    assert result == 12156
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
    assert result == 10835
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
