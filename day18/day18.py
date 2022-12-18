#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 18
#
from typing import Sequence, Iterable, Union, Optional, Any, Dict, List, Tuple, Set
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
1,1,1
2,1,1
        """,
        10
    ),
    (
        """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
        """,
        64
    ),
]

SAMPLE_CASES2 = [
    (
        """
1,1,1
2,1,1
        """,
        10
    ),
    (
        """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
        """,
        58
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

@dataclass(order=True, frozen=True)
class XYZ():
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def dist(self, other: "XYZ") -> int:
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)

    @classmethod
    def from_text(cls, text: str) -> "XYZ":
        x, y, z = text.split(",")
        return cls(int(x), int(y), int(z))

    def neighbors(self) -> Iterable["XYZ"]:
        yield XYZ(self.x - 1, self.y, self.z)
        yield XYZ(self.x + 1, self.y, self.z)
        yield XYZ(self.x, self.y - 1, self.z)
        yield XYZ(self.x, self.y + 1, self.z)
        yield XYZ(self.x, self.y, self.z - 1)
        yield XYZ(self.x, self.y, self.z + 1)

class Drop():
    def __init__(self, cubes: List[XYZ]):
        self.cubes = set(cubes)

        self.cavities = []
        self.xmax = max([v.x for v in self.cubes])
        self.xmin = min([v.x for v in self.cubes])
        self.ymax = max([v.y for v in self.cubes])
        self.ymin = min([v.y for v in self.cubes])
        self.zmax = max([v.z for v in self.cubes])
        self.zmin = min([v.z for v in self.cubes])

        self._total_surface_area = 0

    def in_cavity(self, cube) -> bool:
        return any([cube in cavity for cavity in self.cavities])

    def out_of_bounds(self, cube) -> bool:
        if cube.x < self.xmin or cube.x > self.xmax:
            return True
        if cube.y < self.ymin or cube.y > self.ymax:
            return True
        if cube.z < self.zmin or cube.z > self.zmax:
            return True
        return False

    def find_cavities(self):
        for cube in self.cubes:
            for nayb in cube.neighbors():
                if nayb in self.cubes:
                    continue
                if self.in_cavity(nayb):
                    continue
                if self.out_of_bounds(nayb):
                    continue
                self.add_cavity(nayb)

    def add_cavity(self, cube) -> Set[XYZ]:
        assert cube not in self.cubes

        visited = set()
        queue = [cube]
        while queue:
            cube = queue.pop()
            if cube in visited:
                continue
            visited.add(cube)
            for nayb in cube.neighbors():
                if self.out_of_bounds(cube):
                     return []
                if nayb in self.cubes:
                    continue
                if nayb in visited:
                    continue
                queue.append(nayb)
        self.cavities.append(visited)

    def total_surface_area(self) -> int:
        if not self._total_surface_area:
            self._total_surface_area = surface_area(self.cubes)
        return self._total_surface_area

    def external_surface_area(self) -> int:
        result = self.total_surface_area() 
        result -= sum([surface_area(cavity) for cavity in self.cavities])
        return result


def surface_area(cubes: Set[XYZ]) -> int:
    sides = 6 * len(cubes)
    for cube in cubes:
        for nayb in cube.neighbors():
            if nayb in cubes:
                sides -= 1
    return sides

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    drop = Drop([XYZ.from_text(line) for line in lines])
    # print(f"Droplet comprises {len(drop.cubes)} cubes")
    # print(f"{drop.xmin} <= x <= {drop.xmax}")
    # print(f"{drop.ymin} <= y <= {drop.ymax}")
    # print(f"{drop.zmin} <= z <= {drop.zmax}")

    drop.find_cavities()
    # print(f"Drop has {len(drop.cavities)} cavities")

    return drop.external_surface_area()


def solve(lines: Lines) -> int:
    """Solve the problem."""
    drop = Drop([XYZ.from_text(line) for line in lines])
    return drop.total_surface_area()


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
    assert result == 3530
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
    assert result == 2000
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
