#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 13
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
import json
from functools import cmp_to_key

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
        """,
        13
    ),
]

SAMPLE_CASES2 = [
    (
        """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
        """,
        140
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, **kwargs) -> Lines:
    return load_text(Path(infile).read_text(), **kwargs)

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

def parse_pair(lines) -> Tuple[List[Any], List[Any]]:
    left = json.loads(lines[0])
    right = json.loads(lines[1])
    return left, right

LESS, EQUAL, GREATER = -1, 0, 1

def ordered(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return LESS
        elif left == right:
            return EQUAL
        else:
            return GREATER
    
    if isinstance(left, list) and isinstance(right, list):
        for item_left, item_right in zip(left, right):
            cmp = ordered(item_left, item_right)
            if cmp != EQUAL:
                return cmp
        return ordered(len(left), len(right))

    if isinstance(left, int):
        return ordered([left], right)

    if isinstance(right, int):
        return ordered(left, [right])

    raise ValueError(f"bad types: left is {str(type(left))}, right is {str(type(right))}")


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    sects = parse_sections(lines)
    packets = [json.loads(line) for line in lines if line.strip()]
    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=cmp_to_key(ordered))

    result = 1
    for idx, packet in enumerate(packets):
        if packet in ([[2]], [[6]]):
            result *= idx + 1
    return result
    

def solve(lines: Lines) -> int:
    """Solve the problem."""
    sects = parse_sections(lines)
    pairs = []
    for sect in sects:
        pairs.append(parse_pair(sect))

    ordered_pairs = []
    for idx, (left, right) in enumerate(pairs):
        number = idx + 1
        # print(f"\nPair {number}:")
        # print(f"left:  {left}")
        # print(f"right: {right}")
        if ordered(left, right) == LESS:
            ordered_pairs.append(number)
            # print(f"Pair {number} is CORECTLY ORDERED")
    return sum(ordered_pairs)


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text, blank_lines=True)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 5623
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
    assert result == 20570
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE, blank_lines=True)
    part1(input_lines)
    example2()
    part2(input_lines)
