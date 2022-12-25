from typing import Sequence, Union, Optional, Any, Dict, List, Tuple, Iterable
from dataclasses import dataclass

NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"
NESW = [NORTH, EAST, SOUTH, WEST]


Pos = Tuple[int, int]

def neighbor(pos, nesw: str):
    if nesw == NORTH:
        return (pos[0] - 1, pos[1])
    if nesw == SOUTH:
        return (pos[0] + 1, pos[1])
    if nesw == EAST:
        return (pos[0], pos[1] + 1)
    if nesw == WEST:
        return (pos[0], pos[1] - 1)

def neighbors(pos) -> Iterable[Pos]:
    yield (pos[0] - 1, pos[1])
    yield (pos[0], pos[1] + 1)
    yield (pos[0] + 1, pos[1])
    yield (pos[0], pos[1] - 1)
