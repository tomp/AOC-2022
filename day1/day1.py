#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 1
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
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
        """,
        24000
    ),
]


SAMPLE_CASES2 = [
    (
        """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
        """,
        45000
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
    return [line.strip() for line in text.strip("\n").split("\n")]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        line = line.strip()
        if not line:
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    calories = []

    elves = parse_sections(lines)
    for elf, cals in enumerate(elves):
        calories.append((sum(map(int, cals)), elf))
    calories.sort(reverse=True)
    return calories[0][0] + calories[1][0] + calories[2][0]

def solve(lines: Lines) -> int:
    """Solve the problem."""
    calories = {}
    best_elf = -1
    max_cal = -1

    elves = parse_sections(lines)
    for elf, cals in enumerate(elves):
        calories[elf] = sum(map(int, cals))
        if calories[elf] > max_cal:
            best_elf = elf
            max_cal = calories[elf]

    return max_cal


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
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
