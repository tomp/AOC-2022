#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 20
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
1
2
-3
3
-2
0
4
        """,
        3
    ),
]

SAMPLE_CASES2 = [
    (
        """
1
2
-3
3
-2
0
4
        """,
        1623178306
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

class Message():
    def __init__(self, values: List[int]):
        self.values = values
        self.loc = list(range(len(self.values)))

    def at(self, pos):
        i = pos % len(self.values)
        return self.values[i]

    def mix_one(self, orig_loc):
        """Execute one step of the mixing process, for the value that was
        originally at the specified location.  The values and locs are updated
        in place.
        """
        pos = self.loc.index(orig_loc)
        val = self.values[pos]
        self.values = mix(self.values, pos, val)
        self.loc = mix(self.loc, pos, val)

    def mix(self):
        # if len(self.values) < 10:
        #     print(self.values, self.loc)
        for i in range(len(self.values)):
            self.mix_one(i)
            # if len(self.values) < 10:
            #     print(self.values, self.loc)


def grove_coordinates(values):
    idx = values.index(0)
    at1000 = (idx + 1000) % len(values)
    at2000 = (idx + 2000) % len(values)
    at3000 = (idx + 3000) % len(values)
    return values[at1000] + values[at2000] + values[at3000]


def mix(values, pos, delta):
    size = len(values)
    maxpos = size - 1
    
    val = values[pos]
    # verbose = (val == delta) and (len(values) < 10)
    # if verbose:
    #     print(f"--- mix({values}, {pos}, {delta})")
    
    new_pos = (pos + delta) % maxpos
    if new_pos > pos:
        new_pos += 1

    dest = new_pos
    if dest == pos:
        # if verbose:
        #     print(f"value {val} at pos {pos} does not move")
        return values
   
    if dest > pos:
        # if verbose:
        #     print(f"value {val} at pos {pos} moves before pos {dest}")
        return values[:pos] + values[pos+1:dest] + [val] + values[dest:]

    if dest < pos:
        # if verbose:
        #     print(f"value {val} at pos {pos} moves before pos {dest}")
        return values[:dest] + [val] + values[dest:pos] + values[pos+1:]

DECRYPTION_KEY = 811589153

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    values = [v * DECRYPTION_KEY for v in map(int, lines)]
    msg = Message(values)

    for _ in range(10):
        msg.mix()

    return grove_coordinates(msg.values)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    values = list(map(int, lines))
    msg = Message(values)

    msg.mix()

    return grove_coordinates(msg.values)


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
    assert result == 13522
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
    assert result == 17113168880158
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
