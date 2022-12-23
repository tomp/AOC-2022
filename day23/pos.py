from typing import Sequence, Union, Optional, Any, Dict, List, Tuple, Iterable
from dataclasses import dataclass

NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"

Pos = Tuple[int, int]

def direction(pos, nsew: str):
    if nsew == NORTH:
        return (pos[0] - 1, pos[1])
    if nsew == SOUTH:
        return (pos[0] + 1, pos[1])
    if nsew == EAST:
        return (pos[0], pos[1] + 1)
    if nsew == WEST:
        return (pos[0], pos[1] - 1)

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
