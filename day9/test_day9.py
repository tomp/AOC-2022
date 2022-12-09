#!/usr/bin/env python3

import pytest

from day9 import Pos, Delta


CASES = []

def test_pos():
    row, col = -2, 3
    posA = Pos(row, col)
    assert posA.row == row and posA.col == col

def test_delta():
    dr, dc = 5, -7
    deltaA = Delta(dr, dc)
    assert deltaA.dr == dr and deltaA.dc == dc

def test_pos_sub():
    posA = Pos(3, 5)
    posB = Pos(-1, -1)
    assert posA - posB == Delta(4, 6)

def test_pos_add():
    posA = Pos(3, -1)
    deltaA = Delta(5, -7)
    assert posA + deltaA == Pos(8, -8)
    assert deltaA + posA == Pos(8, -8)

    with pytest.raises(ValueError):
        posB = posA + Pos(1, 1)

def test_delta_delta_math():
    deltaA = Delta(3, 5)
    deltaB = Delta(-1, -1)
    assert deltaA + deltaB == Delta(2, 4)
    assert deltaB + deltaA == Delta(2, 4)
    assert deltaA - deltaB == Delta(4, 6)
    assert deltaB - deltaA == Delta(-4, -6)


def test_delta_pos_math():
    posA = Pos(3, 5)
    posB = Pos(-1, -1)
    result = posA - posB
    assert result == Delta(4, 6)

    assert (posB + result) == posA
    assert (posA - result) == posB
