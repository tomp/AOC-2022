#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 17
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from pprint import pprint
import re

INPUTFILE = "input.txt"

NUM_ROCKS2 = 1000000000000

SAMPLE_CASES = [
    (
        """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
        """,
        3068
    ),
]

SAMPLE_CASES2 = [
    (
        """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
        """,
        1514285714288
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


# Rock rows are upside down, from how they would
# be displayed.  This is to accomodate coord system
# where row numbers increase from 0 going upward, 
# rather than increasing downward as usual.
#
ROCKS = [
    [
        "..####.",
    ],
    [
        "...#...",
        "..###..",
        "...#...",
    ],
    [
        "..###..",
        "....#..",
        "....#..",
    ],
    [
        "..#....",
        "..#....",
        "..#....",
        "..#....",
    ],
    [
        "..##...",
        "..##...",
    ],
]

EMPTY, HASH = ".", "#"
EMPTY_ROW = "......."
BOTTOM_ROW = "#######"

LEFT, RIGHT = "<", ">"


class Rock():
    def __init__(self, rock_type: int = 0, bottom: int = 0):
        self.rock_type = rock_type
        self.bottom = bottom
        self.grid = ROCKS[rock_type]
        self.height = len(self.grid)

    def __repr__(self) -> str:
        return f"Rock({self.rock_type}, {self.bottom})"

    def __str__(self) -> str:
        rows = []
        for rownum in range(self.top, self.bottom - 1, -1):
            rows.append(f"{rownum:4d} |{self.row(rownum)}|")
        return "\n".join(rows)

    @property
    def top(self) -> int:
        return self.bottom + self.height - 1

    def down(self):
        self.bottom -= 1
        return self

    def up(self):
        self.bottom += 1
        return self

    def row(self, rownum: int) -> str:
        if self.bottom <= rownum <= self.top:
            return self.grid[rownum - self.bottom]
        return EMPTY_ROW

    def left(self):
        if not any([row[0] == HASH for row in self.grid]):
            rows = []
            for row in self.grid:
                rows.append(row[1:] + EMPTY)
            self.grid = rows
        return self

    def right(self):
        if not any([row[-1] == HASH for row in self.grid]):
            rows = []
            for row in self.grid:
                rows.append(EMPTY + row[:-1])
            self.grid = rows
        return self

    def collision(self, other: "Rock") -> bool:
        if self.bottom > other.top or self.top < other.bottom:
            return False
        rowmin, rowmax = max(self.bottom, other.bottom), min(self.top, other.top)
        for rownum in range(rowmin, rowmax+1):
            # print(f"{rownum}  |{self.row(rownum)}|  |{other.row(rownum)}|")
            for ch1, ch2 in zip(self.row(rownum), other.row(rownum)):
                if ch1 == HASH and ch2 == HASH:
                    return True
        return False


class RockPile():
    def __init__(self):
        self.rocks: List[Rock] = []
        self.top = 0

    def add_rock(self, rock):
        self.rocks.append(rock)
        if rock.top > self.top:
            self.top = rock.top

    def collision(self, other: Rock) -> bool:
        if any([other.collision(rock) for rock in self.rocks[::-1]]):
            return True
        return other.bottom < 1

    def row(self, rownum: int) -> str:
        rows = [rock.row(rownum) for rock in self.rocks
                if rock.bottom <= rownum and rock.top >= rownum]
        if not rows:
            return EMPTY_ROW
        if len(rows) == 1:
            return rows[0]

        row = []
        for cells in zip(*rows):
            if HASH in cells:
                row.append(HASH)
            else:
                row.append(EMPTY)
        return "".join(row)

def run(wind: str, num_rocks: int = 11):
    pass

def display(pile: RockPile, rock: Rock, title: str = ""):
    """Print a representation of the rock pile and one
    falling rock to the console.
    """
    if title:
        print(title)
    rowmax = max(pile.top, rock.top)
    for rownum in range(rowmax, 0, -1):
        # print(f"--- row {rownum}:  {pile.row(rownum)}  {rock.row(rownum)}")
        row = []
        for ch1, ch2 in zip(pile.row(rownum), rock.row(rownum)):
            if ch1 == HASH or ch2 == HASH:
                row.append(HASH)
            else:
                row.append(ch1)
        print(f"|{''.join(row)}|  {rownum:3d}")
    print(f"|{BOTTOM_ROW}|  {0:3d}")


def solve2(lines: Lines, num_rocks: int) -> int:
    """Solve the problem."""
    wind = lines[0]
    pile = RockPile()
    
    last_height = 0
    height_delta = []
    height_rocks = defaultdict(list)
    rocks_height = {}

    period = 0
    confirmations = 0

    t = 0
    for i in range(10000):
        rock = Rock(i % len(ROCKS), pile.top + 4)
        # display(pile, rock, title=f"\nStep {t:03d};  ({blowing})")
        while True:
            blowing = wind[t % len(wind)]
            t += 1
            if blowing == LEFT:
                rock.left()
                if pile.collision(rock):
                    rock.right()
            else:
                rock.right()
                if pile.collision(rock):
                    rock.left()
            rock.down()
            if pile.collision(rock):
                pile.add_rock(rock.up())
                assert i + 1 == len(pile.rocks)

                # rock has been added
                height_delta.append(pile.top - last_height)
                height_tag = '_'.join(map(str,height_delta[-20:]))
                # print(f"{i+1:4d}, {t}, {len(pile.rocks)}, {pile.top}, {height_tag}")

                height_rocks[height_tag].append(len(pile.rocks))
                rocks_height[len(pile.rocks)] = pile.top

                if len(height_rocks[height_tag]) > 3:
                    rocks2 = height_rocks[height_tag][-1]
                    rocks1 = height_rocks[height_tag][-2]
                    if rocks2 - rocks1 == period:
                        confirmations += 1
                    else:
                        period = rocks2 - rocks1
                        confirmations = 0

                    if confirmations > 100:
                        # print(f"### We have a confirmed period of {period} in the height increases.")
                        periods = num_rocks // period
                        offset = num_rocks % period
                        delta = rocks_height[rocks2] - rocks_height[rocks1]

                        # print(f"--- period={period}  offset={offset}  periods={periods} delta={delta}")
                        assert offset + (period * periods) == num_rocks

                        while offset + period < len(pile.rocks):
                            periods -= 1
                            offset += period
                        assert offset + (period * periods) == num_rocks

                        result = rocks_height[offset] + (delta * periods)
                        # print(f"!!! height at {num_rocks} should be {result}")
                        return result


                last_height = pile.top
                break

    return pile.top

def solve(lines: Lines) -> int:
    """Solve the problem."""
    wind = lines[0]
    pile = RockPile()
    
    t = 0
    for i in range(2022):
        rock = Rock(i % len(ROCKS), pile.top + 4)
        # display(pile, rock, title=f"\nStep {t:03d};  ({blowing})")
        while True:
            blowing = wind[t % len(wind)]
            t += 1
            if blowing == LEFT:
                rock.left()
                if pile.collision(rock):
                    rock.right()
            else:
                rock.right()
                if pile.collision(rock):
                    rock.left()
            rock.down()
            if pile.collision(rock):
                pile.add_rock(rock.up())

                # rock has been added
                # print(f"{i+1:4d} rocks @ t={t}, height={pile.top}")
                break

    return pile.top


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
    assert result == 3083
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines, NUM_ROCKS2)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines, NUM_ROCKS2)
    print(f"result is {result}")
    assert result == 1532183908048
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
