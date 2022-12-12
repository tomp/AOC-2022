#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 12
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from heapq import heapify, heappush, heappop
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
        """,
        31
    ),
]

SAMPLE_CASES2 = [
    (
        """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
        """,
        29
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

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col),
        ]

    def dist(self, other: "Pos") -> int:
        return abs(other.row - self.row) + abs(other.col - self.col)


Grid = Dict[Pos, int]

START, END = "S", "E"
LOWEST = 0
HIGHEST = ord('z') - ord('a')

class Board():
    grid: Grid

    def __init__(self, cells: Grid, start: Pos, target: Pos):
        self.grid = cells
        self.rowmax = max([v.row for v in self.grid.keys()])
        self.rowmin = min([v.row for v in self.grid.keys()])
        self.colmax = max([v.col for v in self.grid.keys()])
        self.colmin = min([v.col for v in self.grid.keys()])

        self.start = start
        self.target = target

    @classmethod
    def from_lines(cls, lines, **kwargs) -> "Board":
        grid = defaultdict(lambda : HIGHEST + 2)
        for r, line in enumerate(lines):
            for c, val in enumerate(line):
                if val == START:
                    start = Pos(r, c)
                    grid[Pos(r, c)] = LOWEST
                elif val == END:
                    target = Pos(r, c)
                    grid[Pos(r, c)] = HIGHEST
                else:
                    grid[Pos(r, c)] = ord(val) - ord('a')
        return cls(grid, start=start, target=target, **kwargs)

    def print(self, title="", overlay=None):
        if title:
            print(title)
        for r in range(self.rowmin, self.rowmax+1):
            row = []
            for c in range(self.colmin, self.colmax+1):
                pos = Pos(r, c)
                val = chr(self.grid[pos] + ord('a'))
                if overlay and pos in overlay:
                    val = overlay[pos]
                row.append(val)
            print("".join(row))


def shortest_path_to_target(board, start, target) -> List[Pos]:
    """Run an A* search (breadth-first search with minimum distance heuristic)
    to find the shortest path from the starting position to the target location.
    """
    visited = set()
    queue = [(start.dist(target), start, [])]
    heapify(queue)
    while queue:
        score, pos, hist = heappop(queue)
        if pos in visited:
            continue
        # print(f">>> check {pos}  score={score} height={board.grid[pos]}")
        if pos == target:
            return hist
        visited.add(pos)
        height = board.grid[pos]
        for nayb in pos.neighbors():
            if board.grid[nayb] <= height + 1 and nayb not in visited:
                nayb_score = len(hist) + nayb.dist(target)
                # print(f"... neighbor {nayb}  score={nayb_score}  height={board.grid[nayb]}")
                heappush(queue, (nayb_score, nayb, hist + [nayb]))
    return []


def shortest_path_to_base(board, start) -> List[Pos]:
    """Run a breadth-first search to find the shortest path from the
    starting position to a location with height 0.
    """
    visited = set()
    queue = [(start, [])]
    while queue:
        pos, hist = queue.pop(0)
        if pos in visited:
            continue
        height = board.grid[pos]
        # print(f">>> check {pos}  height={height}")
        if height == LOWEST:
            return hist
        visited.add(pos)
        for nayb in pos.neighbors():
            nayb_height = board.grid[nayb]
            if height <= nayb_height + 1 and nayb not in visited:
                # print(f"... neighbor {nayb}  height={nayb_height}")
                queue.append((nayb, hist + [nayb]))
    return []


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    # board.print(title="Initially")
    path = shortest_path_to_base(board, board.target)
    return len(path)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    board = Board.from_lines(lines)
    # board.print(title="Initially")
    path = shortest_path_to_target(board, board.start, board.target)
    return len(path)


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
    assert result == 440
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
    assert result == 439
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
