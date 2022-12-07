#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 7
#
from typing import Sequence, Union, Optional, Any, Dict, List
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

DISK_SIZE = 70000000
MIN_SIZE = 30000000
SIZE_THRESHOLD = 100000

SAMPLE = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

"""

EXPECTED = 95437

SAMPLE2 = SAMPLE
EXPECTED2 = 24933642


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

PROMPT = "$"
CD = "cd"
LS = "ls"
DIR = "dir"
SLASH = "/"
DOTDOT = ".."


def parse_commands(lines: Lines) -> Dict[str, int]:
    files = {}
    cwd = Path("/")

    listing = False
    for line in lines:
        # print(f">>> {line}")
        words = line.split()
        if words[0] == PROMPT:
            cmd = words[1]
            listing = False
            if cmd == CD:
                name = words[2]
                if name == SLASH:
                    cwd = Path("/")
                elif name == DOTDOT:
                    cwd = cwd.parent
                else:
                    cwd = cwd / Path(name)
                continue

            if cmd == LS:
                listing = True
                continue

            raise ValueError(f"Unrecognized command '{cmd}'")

        else:
            assert listing
            name = words[1]
            filepath = str(cwd / Path(name))

            if words[0] == DIR:
                continue
            size = int(words[0])
            files[filepath] = size

    return files
        


def directory_sizes(files: Dict[str, int]) -> Dict[str, int]:
    dirsize = defaultdict(int)

    print("--- files ---")
    for filepath, size in sorted(files.items()):
        # print(f"{size:-8d}  {filepath}")
        dirpath, filename = filepath.rsplit(SLASH, maxsplit=1)
        dirsize[dirpath] += size
        # print(f"ADD {size:-8d} {dirpath}")
        while dirpath:
            dirpath, dirname = dirpath.rsplit(SLASH, maxsplit=1)
            dirsize[dirpath] += size
            # print(f"ADD {size:-8d} {dirpath}")

    return dirsize

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    files = parse_commands(lines)
    dirsize = directory_sizes(files)
    need = MIN_SIZE - (DISK_SIZE - dirsize[""])
    print(f"We need to find {need} bytes")

    dirs = []
    for dirpath, size in dirsize.items():
        if size >= need:
            dirs.append((size, dirpath))
    dirs.sort()

    size, dirpath = dirs[0]
    print(f"This will work: {dirpath}  size: {size}")

    return size

def solve(lines: Lines) -> int:
    """Solve the problem."""
    files = parse_commands(lines)
    # print("--- files ---")
    # for filepath, size in sorted(files.items()):
    #     print(f"{size:-8d}  {filepath}")

    dirsize = directory_sizes(files)
    # print("--- directories ---")
    total = 0
    for dirpath, size in sorted(dirsize.items()):
        # print(f"{size:-12d} {dirpath}")
        if dirpath and size <= SIZE_THRESHOLD:
            total += size

    return total


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    text, expected = SAMPLE, EXPECTED
    lines = load_text(text)
    result = solve(lines)
    print(f"'{text}' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 1915606
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    text, expected = SAMPLE2, EXPECTED2
    lines = load_text(text)
    result = solve2(lines)
    print(f"'{text}' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 5025657
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
