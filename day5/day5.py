#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 5
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
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
        """,
        "CMZ"
    ),
]

SAMPLE_CASES2 = [
    (
        """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
        """,
        "MCD"
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

## Use these if blank lines in input are meaningful.

def load_text(text: str) -> Lines:
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

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    lines, procedure = parse_sections(lines)
    stack = parse_stack(lines)
    step = 0
    for line in procedure:
        if not line:
            continue
        step += 1
        # print(f"STEP {step}")
        # print_stack(stack)
        count, a, b = parse_instruction(line)
        move_crates(stack, a-1, b-1, count)
    result = "".join([crates[-1] for crates in stack if crates])
    return result

def parse_stack(lines):
    nstack = (max([len(line) for line in lines]) + 1) // 4
    stack = [[] for _ in range(nstack)]
    for line in reversed(lines[:-1]):
        for i in range(nstack):
            if i*4+1 < len(line):
                crate = line[i*4+1]
                if crate != " ":
                    stack[i].append(crate)
    return stack

def parse_instruction(line):
    words = line.split()
    assert words[0] == "move" and words[2] == "from" and words[4] == "to"
    return int(words[1]), int(words[3]), int(words[5])

def print_stack(stack):
    for i, crates in enumerate(stack):
        print(f"{i+1:2d}: {' '.join(stack[i])}")

def move_crate(stack, a, b):
    crate = stack[a].pop(-1)
    stack[b].append(crate)

def move_crates(stack, a, b, count):
    crates = stack[a][-count:]
    stack[b].extend(crates)
    stack[a] = stack[a][:-count]

def solve(lines: Lines) -> int:
    """Solve the problem."""
    lines, procedure = parse_sections(lines)
    stack = parse_stack(lines)
    step = 0
    for line in procedure:
        if not line:
            continue
        step += 1
        # print(f"STEP {step}")
        # print_stack(stack)
        count, a, b = parse_instruction(line)
        for _ in range(count):
            move_crate(stack, a-1, b-1)
    result = "".join([crates[-1] for crates in stack if crates])
    return result


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
    assert result == "CVCWCRTVQ"
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
    assert result == "CNSCZWLVT"
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
