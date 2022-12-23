from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from dataclasses import dataclass
NORTH, SOUTH, EAST, WEST = "N", "S", "E", "W"

@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def dist(self, other: "Pos") -> int:
        return abs(other.row - self.row) + abs(other.col - self.col)

    def direction(self, nsew: str):
        if nsew == NORTH:
            return Pos(self.row - 1, self.col)
        if nsew == SOUTH:
            return Pos(self.row + 1, self.col)
        if nsew == EAST:
            return Pos(self.row, self.col + 1)
        if nsew == WEST:
            return Pos(self.row, self.col - 1)

    def neighbors(self, nsew: str = "") -> "List[Pos]":
        if not nsew:
            return [
                Pos(self.row, self.col + 1),
                Pos(self.row + 1, self.col + 1),
                Pos(self.row + 1, self.col),
                Pos(self.row + 1, self.col - 1),
                Pos(self.row, self.col - 1),
                Pos(self.row - 1, self.col - 1),
                Pos(self.row - 1, self.col),
                Pos(self.row - 1, self.col + 1),
            ]
        if nsew == NORTH:
            return [
                Pos(self.row - 1, self.col - 1),
                Pos(self.row - 1, self.col),
                Pos(self.row - 1, self.col + 1),
            ]
        if nsew == SOUTH:
            return [
                Pos(self.row + 1, self.col + 1),
                Pos(self.row + 1, self.col),
                Pos(self.row + 1, self.col - 1),
            ]
        if nsew == EAST:
            return [
                Pos(self.row - 1, self.col + 1),
                Pos(self.row, self.col + 1),
                Pos(self.row + 1, self.col + 1),
            ]
        if nsew == WEST:
            return [
                Pos(self.row + 1, self.col - 1),
                Pos(self.row, self.col - 1),
                Pos(self.row - 1, self.col - 1),
            ]
