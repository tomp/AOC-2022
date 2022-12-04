#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 4
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
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
        """,
        2
    ),
]

SAMPLE_CASES2 = [
    (
        """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
        """,
        4
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

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    total = 0
    for line in lines:
        ids1, ids2 = parse_line(line)
        if ids1[0] > ids2[0]:
            ids1, ids2 = ids2, ids1
        # print(f"{ids1} :: {ids2}")
        if ids2[0] <= ids1[1]:
            # print("^^^ overlap")
            total += 1
    return total

def parse_line(line):
    return [list(map(int, part.split("-"))) for part in line.split(",")]

def solve(lines: Lines) -> int:
    """Solve the problem."""
    total = 0
    for line in lines:
        ids1, ids2 = parse_line(line)
        if ids1[1] - ids1[0] < ids2[1] - ids2[0]:
            ids1, ids2 = ids2, ids1
        # print(f"{ids1} :: {ids2}")
        if ids1[0] <= ids2[0] and ids1[1] >= ids2[1]:
            # print("^^^ contains")
            total += 1
    return total


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
    assert result == 528
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
    assert result == 881
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
