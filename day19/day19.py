#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 19
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict, ChainMap
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian.
        """,
        33
    ),
]

SAMPLE_CASES2 = SAMPLE_CASES


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

NUMBER_RE = re.compile(r"Blueprint (\d+): ")
ORE_COST_RE = re.compile(r"Each ore robot costs (\d+) ore")
CLAY_COST_RE = re.compile(r"Each clay robot costs (\d+) ore")
OBSIDIAN_COST_RE = re.compile(r"Each obsidian robot costs (\d+) ore and (\d+) clay")
GEODE_COST_RE = re.compile(r"Each geode robot costs (\d+) ore and (\d+) obsidian")


ORE, CLAY, OBSIDIAN, GEODE = "ore", "clay", "obsidian", "geode"
ROBOTS = (GEODE, OBSIDIAN, CLAY, ORE)
MATERIALS = (ORE, CLAY, OBSIDIAN)
ITEMS = (ORE, CLAY, OBSIDIAN, GEODE)

class Blueprint():
    def __init__(self, number: int, cost: Dict[str, Dict[str, int]]):
        self.cost = cost
        self.number = number

    # @classmethod
    # def from_text_v0(cls, text: str) -> "Blueprint":
    #     print(f">>> {text}")
    #     number = int(NUMBER_RE.match(text).group(1))
    #     ore_cost = Cost(*[int(val) for val in ORE_COST_RE.search(text).groups()])
    #     clay_cost = Cost(*[int(val) for val in CLAY_COST_RE.search(text).groups()])
    #     obsidian_cost = Cost(*[int(val) for val in CLAY_COST_RE.search(text).groups()])
    #     vals = [int(val) for val in GEODE_COST_RE.search(text).groups()]
    #     geode_cost = Cost(vals[0], 0, vals[1])
    #     return cls(number, {ORE: ore_cost, CLAY: clay_cost, OBSIDIAN: obsidian_cost, GEODE: geode_cost})

    @classmethod
    def from_text(cls, text: str) -> "Blueprint":
        print(f">>> {text}")
        number = int(NUMBER_RE.match(text).group(1))

        vals = [int(val) for val in ORE_COST_RE.search(text).groups()]
        ore_cost = {ORE: vals[0], CLAY: 0, OBSIDIAN: 0}

        vals = [int(val) for val in CLAY_COST_RE.search(text).groups()]
        clay_cost = {ORE: vals[0], CLAY: 0, OBSIDIAN: 0}

        vals = [int(val) for val in OBSIDIAN_COST_RE.search(text).groups()]
        obsidian_cost = {ORE: vals[0], CLAY: vals[1], OBSIDIAN: 0}

        vals = [int(val) for val in GEODE_COST_RE.search(text).groups()]
        geode_cost = {ORE: vals[0], CLAY: 0, OBSIDIAN: vals[1]}

        return cls(number, {ORE: ore_cost, CLAY: clay_cost, OBSIDIAN: obsidian_cost, GEODE: geode_cost})

def round_up(number) -> int:
    return int(math.ceil(max(number, 0)))


class Execution():
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.resources: Dict[str, int] = defaultdict(int)
        self.robots: Dict[str, int] = defaultdict(int)
        self.robots[ORE] = 1
        self.step = 0

    def quality(self) -> int:
        while self.step < 24:
            self.single_step()
        return self.resources[GEODE] * self.blueprint.number

    def run(self, steps: int = 1):
        for _ in range(steps):
            self.single_step()

    def single_step(self):
        # aliases
        cost = self.blueprint.cost
        resources = self.resources
        robots = self.robots

        self.step += 1
        print(f"== Minute {self.step} ==")

        new_robot = None
        next_robot = {}
        blocker = ""
        for robot in ROBOTS:
            # do we have robots producing all of the material for this next robot?
            if all([robots[item] for item, amount in cost[robot].items() if amount]):
                steps, blocker = build_time(robot, robots, resources, cost)

                if steps == 0:
                    print(f"We can build a new {robot}-collecting robot now.")
                else:
                    print(f"We'll be able to build a {robot}-collecting robot in {steps} steps")
                next_robot[robot] = steps

                steps2, _ = build_time(robot, robots, resources, cost, add_robot=blocker)
                if steps2 >= steps:
                    blocker = ""

                if steps == 0 and new_robot is None and robot == blocker:
                    new_robot = robot
                    new_robot_steps = steps

            # how to decide when to build more clay robots and when to just wait...?

            else:
                print(f"We can't build {robot}-collecting robots yet")
                next_robot[robot] = None

        if new_robot and new_robot_steps == 0:
            spend = {
                item: cost[new_robot][item] for item in MATERIALS if cost[new_robot][item]
            }
            print(describe_spend(new_robot, spend))
            for item, amount in spend.items():
                resources[item] -= amount

        # collect resources with existing robots
        for item, count in robots.items():
            if count:
                resources[item] += count
                print(f"{count} {item}-collecting robots collect {count} {item}; "
                      f"You now have {resources[item]} {item}.")
   
        if new_robot and new_robot_steps == 0:
            robots[new_robot] += 1
            print(f"The new {new_robot}-collecting robot is ready; "
                  f"You now have {robots[new_robot]} of them.")
       

def build_time(target_robot: str, robots, resources, cost, add_robot: Optional[str] = None) -> Tuple[int, str]:
    if not add_robot:
        build_robots = robots
        build_resources = resources
    else:
        build_robots = {name: count if name != add_robot else count + 1 for name, count in robots.items()}
        build_resources = {item: amount - cost[add_robot][item] for item, amount in build_resources.items()}
    steps = 0
    max_item_steps = 0
    blocker = ""
    for item, amount in cost[target_robot].items():
        if build_robots[item]:
            item_steps = round_up((cost[target_robot][item] - build_resources[item]) / build_robots[item])
            if item_steps > steps:
                steps = item_steps
            if item_steps > max_item_steps:
                max_item_steps = item_steps
                blocker = item
    return steps, blocker

def describe_spend(robot, spend) -> str:
    parts = ["Spend"]
    parts.append(" and ".join([f"{count} {item}" for item, count in spend.items() if count]))
    parts.append(f"to start building a {robot}-collecting robot.")
    return " ".join(parts)


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    blueprints = [Blueprint.from_text(line) for line in lines]
    engine = Execution(blueprints[0])
    engine.run(24)
    return engine.quality()


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
    assert result == -1
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
    assert result == -1
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
