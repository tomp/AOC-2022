#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 6
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
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        7
    ),
    (
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        5
    ),
    (
        "nppdvjthqldpwncqszvftbrmjlhg",
        6
    ),
    (
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        10
    ),
    (
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
        11
    ),
]

SAMPLE_CASES2 = [
    (
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        19
    ),
    (
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        23
    ),
    (
        "nppdvjthqldpwncqszvftbrmjlhg",
        23
    ),
    (
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        29
    ),
    (
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
        26
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

def solve2(text: str) -> int:
    """Solve the problem."""
    i = 0
    j = 0
    size = len(text)
    while j < size:
        j += 1
        # print(f"{i}:{j} '{text[i:j+1]}'")
        ch = text[j]
        if ch in text[i:j]:
            i = i + 1 + text[i:j].index(ch)
        elif j - i == 13:
            break
    return j+1

def solve(text: str) -> int:
    """Solve the problem."""
    i = 0
    j = 0
    size = len(text)
    while j < size:
        j += 1
        # print(f"{i}:{j} '{text[i:j+1]}'")
        ch = text[j]
        if ch in text[i:j]:
            i = i + 1 + text[i:j].index(ch)
        elif j - i == 3:
            break
    return j+1


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        line = load_text(text)[0]
        result = solve(line)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines[0])
    print(f"result is {result}")
    assert result == 1987
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        line = load_text(text)[0]
        result = solve2(line)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines[0])
    print(f"result is {result}")
    assert result == 3059
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
