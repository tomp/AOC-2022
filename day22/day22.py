#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 22
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from pprint import pprint
from collections import defaultdict
from dataclasses import dataclass
import math
import re

from pos import Pos, NORTH, SOUTH, EAST, WEST, neighbor, turn


INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
        """,
        6032
    ),
]

SAMPLE_CASES2 = [
    (
        """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
        """,
        5031
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(Path(infile).read_text(), strip=strip, blank_lines=blank_lines)

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

EMPTY, OPEN, WALL = " ", ".", "#"

Turn = str
Heading: str
Distance = int
Route = List[Union[Turn, Distance]]


class Board():
    def __init__(self, tiles):
        self.tiles = tiles
        self.maxrow = len(self.tiles) - 1
        self.maxcol = len(self.tiles[0]) - 1

        self.loc = self.start_pos()
        self.heading = EAST
        self.trace = [(self.loc, self.heading)]

    @property
    def size(self) -> Tuple[int, int]:
        """Return (nrows, ncols) tuple."""
        return len(self.tiles), max([len(row) for row in self.tiles])

    def display(self, title: str = ""):
        if title:
            print(f"== {title} ==")
        for row in self.tiles:
            print(row)

    def start_pos(self) -> Pos:
        for r, row in enumerate(self.tiles):
            c = row.index(OPEN)
            if c >= 0:
                return (r, c)
        return None
 
    def password(self) -> int:
        r, c = self.loc
        facing = {NORTH: 3, EAST: 0, SOUTH: 1, WEST: 2}[self.heading]
        return (1000 * (r + 1)) + (4 * (c + 1)) + facing

    def follow_route(self, route: Route):
        # print(f"location: {self.loc}  heading: {self.heading}")
        self.trace = [(self.loc, self.heading)]
        for step in route:
            self.single_step(step)
            # print(f"location: {self.loc}  heading: {self.heading}")
        
    def single_step(self, where: Union[str, int]):
        """Either step forward N tiles (or until you're blocked by a wall)
        or change your heading to the right or left.
        """
        if isinstance(where, int):
            # print(f"step forward {where} tiles...")
            self.step_forward(where)
        else:
            # print(f"turn {where} ...")
            self.heading = turn(self.heading, where)
            self.trace.append((self.loc, self.heading))
            # print(f"location: {self.loc}  heading: {self.heading}")

    def neighbor(self, loc, heading) -> Pos:
        next_loc = neighbor(loc, heading)
        r, c = next_loc
        if r < 0:
            r = self.maxrow
        elif r > self.maxrow:
            r = 0
        if c < 0:
            c = self.maxcol
        elif c > self.maxcol:
            c = 0
        # print(f"... neighbor({loc}) -> {next_loc} -> {(r, c)}")
        return (r, c)

    def step_forward(self, nsteps: int):
        for _ in range(nsteps):
            next_loc = self.neighbor(self.loc, self.heading)
            tile = self.tiles[next_loc[0]][next_loc[1]]
            if tile == EMPTY:
                while tile == EMPTY:
                    next_loc = self.neighbor(next_loc, self.heading)
                    tile = self.tiles[next_loc[0]][next_loc[1]]
            if tile == OPEN:
                self.loc = next_loc
                self.trace.append((self.loc, self.heading))
                # print(f"location: {self.loc}  heading: {self.heading}")
            elif tile == WALL:
                # print(f"blocked by wall at {next_loc}")
                break



BOARD_RE = re.compile(r"^([ ]*)([.#]+)([ ]*)$")

def parse_lines2(lines: Lines) -> Board:
    tiles = []

    # get info to work out how the box folds up...
    patt = defaultdict(int)
    for line in lines:
        print(f">>> '{line}'")
        parts = list(map(len, BOARD_RE.match(line).groups()))
        if not patt or parts != patt[-1]:
            patt.append(parts)
    pprint(patt)

    for line in lines:
        tiles.append(line)
    return Board(tiles)

def parse_lines(lines: Lines) -> Board:
    ncol = max([len(line) for line in lines])
    tiles = []
    for line in lines:
        if len(line) < ncol:
            line = line + EMPTY * (ncol - len(line))
        tiles.append(line)
    return Board(tiles)

STEP_RE = re.compile(r"(\d+|[RL])(.*)$")

RIGHT, LEFT = "R", "L"

def parse_directions(text: str) -> List[Union[str, int]]:
    result = []
    match = STEP_RE.match(text)
    while text and match:
        field = match.group(1)
        if field in (RIGHT, LEFT):
            result.append(field)
        else:
            result.append(int(field))
        text = match.group(2)
        match = STEP_RE.match(text)
    if text:
        raise ValueError(f"unparseable input: '{text}'")
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    parts = parse_sections(lines)
    board = parse_lines2(parts[0])
    route = parse_directions(parts[1][0])

    if board.size[1] < 40:
        board.display("Initially")

    board.follow_route(route)

    return board.password()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    parts = parse_sections(lines)
    board = parse_lines(parts[0])
    route = parse_directions(parts[1][0])

    if board.size[1] < 40:
        board.display("Initially")

    board.follow_route(route)

    return board.password()


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text, blank_lines=True, strip=False)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 103224
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text, blank_lines=True, strip=False)
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
    input_lines = load_input(INPUTFILE, strip=False, blank_lines=True)
    part1(input_lines)
    example2()
    part2(input_lines)
