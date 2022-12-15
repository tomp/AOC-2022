#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 15
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ((
        """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
        """, 
        10
     ),
        26
    ),
]

SAMPLE_CASES2 = [
    ((
        """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
        """, 
        20
     ),
        56000011
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
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def dist(self, other: "Pos") -> int:
        return abs(other.row - self.row) + abs(other.col - self.col)


EMPTY, SENSOR, BEACON = ".", "S", "B"

INPUT_RE = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$"
)

def parse_lines(lines) -> Dict[Pos, Pos]:
    sensors: Dict[Pos, Pos] = {}  # nearest beacon to sensor
    for line in lines:
        xs, ys, xb, yb = INPUT_RE.match(line).groups()
        sensor_pos = Pos(int(ys), int(xs))
        beacon_pos = Pos(int(yb), int(xb))
        sensors[sensor_pos] = beacon_pos
    return sensors


@dataclass(order=True, frozen=True)
class Region():
    start: int
    end: int

    def __repr__(self) -> str:
        return f"({self.start}->{self.end})"

    def size(self) -> int:
        return self.end - self.start + 1

    def union(self, other: "Region") -> "Region":
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        if end - start + 1 < self.size() + other.size():
            return Region(start, end)
        raise ValueError(f"Union can't merge {self} and {other}")

    def disjoint(self, other: "Region") -> bool:
        return self.end < other.start or other.end < self.start

    def includes(self, val: int) -> bool:
        return self.start <= val <= self.end


def solve2(lines: Lines, max_xy: int) -> int:
    """Solve the problem."""
    sensors = parse_lines(lines)
    beacons = set(sensors.values())
    # print(f"We know about {len(sensors)} sensors and {len(beacons)} beacons")

    radius = {sensor: sensor.dist(beacon) for sensor, beacon in sensors.items()}
    # for sensor, beacon in sensors.items():
    #     print(f"sensor {sensor} --> beacon {beacon}  distance is {radius[sensor]}")

    possible = None
    for row in range(max_xy+1):
        regions = []
        for sensor, rad in radius.items():
            dr = abs(sensor.row - row)
            if rad < dr:
                continue
            dc = rad - dr
            regions.append(Region(sensor.col - dc, sensor.col + dc))
            # print(f"excluded region for sensor {sensor} (rad {rad}) is {regions[-1]}")
        regions.sort()

        colmin = max(0, min([v.start for v in regions]))
        colmax = min(max_xy, max([v.end for v in regions]))
        # print(f"Search columns {colmin} to {colmax} of row {row} for excluded locations...")
        col = colmin
        covered = []
        while col < colmax + 1:
            included = 0
            for region in regions:
                 if region.includes(col):
                     included += 1
                     col = region.end + 1
            if not included:
                possible = Pos(row, col)
                print(f"possible beacon @ {Pos(row, col)}")
                break

        if possible:
            return tuning_frequency(possible)

    return -1


def tuning_frequency(pos: Pos) -> int:
    return pos.row + 4000000 * pos.col


def solve(lines: Lines, row) -> int:
    """Solve the problem."""
    sensors = parse_lines(lines)
    beacons = set(sensors.values())
    # print(f"We know about {len(sensors)} sensors and {len(beacons)} beacons")

    radius = {sensor: sensor.dist(beacon) for sensor, beacon in sensors.items()}
    # for sensor, beacon in sensors.items():
    #     print(f"sensor {sensor} --> beacon {beacon}  distance is {radius[sensor]}")

    regions = []
    for sensor, rad in radius.items():
        dr = abs(sensor.row - row)
        if rad < dr:
            continue
        dc = rad - dr
        regions.append(Region(sensor.col - dc, sensor.col + dc))
        # print(f"excluded region for sensor {sensor} (rad {rad}) is {regions[-1]}")
    regions.sort()

    colmin = min([v.start for v in regions])
    colmax = max([v.end for v in regions])
    # print(f"Search columns {colmin} to {colmax} of row {row} for excluded locations...")
    possible = 0
    col = colmin
    covered = []
    while col < colmax + 1:
        included = 0
        for region in regions:
             if region.includes(col):
                 included += 1
                 col = region.end + 1
        if not included:
            possible += 1
            # print(f"possible beacon @ {Pos(row, col)}")
            col += 1

    for beacon in beacons:
        if beacon.row == row:
            for region in regions:
                if region.includes(beacon.col):
                    possible += 1
                    break

    excluded = colmax - colmin - possible + 1
    return excluded


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for (text, row), expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines, row)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    ROW = 2000000
    result = solve(lines, ROW)
    print(f"result is {result}")
    assert result == 5144286
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for (text, max_xy), expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines, max_xy)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    MAX_XY = 4000000
    result = solve2(lines, MAX_XY)
    print(f"result is {result}")
    assert result == 10229191267339
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
