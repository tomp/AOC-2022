#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 19
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
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
        """,
        33
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

NUMBER_RE = re.compile(r"Blueprint (\d+): ")
ORE_COST_RE = re.compile(r"Each ore robot costs (\d+) ore")
CLAY_COST_RE = re.compile(r"Each clay robot costs (\d+) ore")
OBSIDIAN_COST_RE = re.compile(r"Each obsidian robot costs (\d+) ore and (\d+) clay")
GEODE_COST_RE = re.compile(r"Each geode robot costs (\d+) ore and (\d+) obsidian")


ORE, CLAY, OBSIDIAN, GEODE = "ore", "clay", "obsidian", "geode"

@dataclass
class Cost():
    ore: int
    clay: int = 0
    obsidian: int = 0


class Blueprint():
    def __init__(self, number: int, cost: Dict[str, Cost]):
        self.cost = cost
        self.number = number

    @classmethod
    def from_text(cls, text: str) -> "Blueprint":
        print(f">>> {text}")
        number = int(NUMBER_RE.match(text).group(1))
        ore_cost = Cost(*[int(val) for val in ORE_COST_RE.search(text).groups()])
        clay_cost = Cost(*[int(val) for val in CLAY_COST_RE.search(text).groups()])
        obsidian_cost = Cost(*[int(val) for val in CLAY_COST_RE.search(text).groups()])
        vals = [int(val) for val in GEODE_COST_RE.search(text).groups()]
        geode_cost = Cost(vals[0], 0, vals[1])
        return cls(number, {ORE: ore_cost, CLAY: clay_cost, OBSIDIAN: obsidian_cost, GEODE: geode_cost})



def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    blueprints = [Blueprint.from_text(line) for line in lines]
    return 0


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
