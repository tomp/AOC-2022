from typing import Sequence, Union, Optional, Any, Dict, List, Tuple, Iterable
from dataclasses import dataclass

NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"
HEADINGS = [NORTH, EAST, SOUTH, WEST]

RIGHT, LEFT = "R", "L"


Pos = Tuple[int, int]

def neighbor(pos, nsew: str):
    if nsew == NORTH:
        return (pos[0] - 1, pos[1])
    if nsew == SOUTH:
        return (pos[0] + 1, pos[1])
    if nsew == EAST:
        return (pos[0], pos[1] + 1)
    if nsew == WEST:
        return (pos[0], pos[1] - 1)

def turn(heading: str, right_left: str):
    idx = HEADINGS.index(heading)
    if right_left == RIGHT:
        return HEADINGS[(idx + 1) % 4]
    elif right_left == LEFT:
        return HEADINGS[(idx - 1) % 4]
    raise ValueError(f"Unrecognized direction '{right_left}'")

def neighbors(pos, nsew: str = "") -> Iterable[Pos]:
    if not nsew:
        yield (pos[0], pos[1] + 1)
        yield (pos[0] + 1, pos[1] + 1)
        yield (pos[0] + 1, pos[1])
        yield (pos[0] + 1, pos[1] - 1)
        yield (pos[0], pos[1] - 1)
        yield (pos[0] - 1, pos[1] - 1)
        yield (pos[0] - 1, pos[1])
        yield (pos[0] - 1, pos[1] + 1)
    if nsew == NORTH:
        yield (pos[0] - 1, pos[1] - 1)
        yield (pos[0] - 1, pos[1])
        yield (pos[0] - 1, pos[1] + 1)
    if nsew == SOUTH:
        yield (pos[0] + 1, pos[1] + 1)
        yield (pos[0] + 1, pos[1])
        yield (pos[0] + 1, pos[1] - 1)
    if nsew == EAST:
        yield (pos[0] - 1, pos[1] + 1)
        yield (pos[0], pos[1] + 1)
        yield (pos[0] + 1, pos[1] + 1)
    if nsew == WEST:
        yield (pos[0] + 1, pos[1] - 1)
        yield (pos[0], pos[1] - 1)
        yield (pos[0] - 1, pos[1] - 1)
