#!/usr/bin/env python3
#
#  Advent of Code 2022 - Day 16
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from heapq import heapify, heappush, heappop
from itertools import combinations
from pprint import pprint
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
        """,
        1651,
    ),
]

SAMPLE_CASES2 = [
    (
        """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
        """,
        1707,
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

LINE_RE = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)$"
)

CLOSED, OPEN = 0, 1
TOTAL_TIME = 30
TOTAL_ELEPHANT_TIME = 26
START = "AA"

DistanceMatrix = Dict[str, Dict[str, int]]


@dataclass
class Valve:
    name: str
    flow: int
    neighbors: List[str]
    dist: Dict[str, int]

    @classmethod
    def from_text(cls, text: str) -> "Valve":
        name, flow, naybs = LINE_RE.match(text).groups()
        nayb_list = naybs.split(", ")
        return cls(name, int(flow), nayb_list, {})


def neighbor_distances(start: str, valves: Dict[str, Valve]) -> Dict[str, int]:
    """Return dict mapping each possible step to a tuple of the time to
    get there.  Valves with flow 0 are ignored - they just contribute to
    the travel time.
    """
    result = {}
    queue = [(0, start)]
    visited = set()
    while queue:
        dist, name = queue.pop(0)
        if name not in visited:
            # print(f"{dist:2d} {name}")
            visited.add(name)
            valve = valves[name]
            if valve.flow or name == START:
                result[name] = dist
            for nayb in valve.neighbors:
                if nayb not in visited:
                    queue.append((dist + 1, nayb))
    return result

def add_distances(valves: Dict[str, Valve]) -> None:
    valves[START].dist = neighbor_distances(START, valves)
    names = [name for name, valve in valves.items() if valve.flow]
    for name in names:
        valves[name].dist = neighbor_distances(name, valves)


def greedy_search(valves) -> Tuple[int, List[str]]:

    print("\n### GREEDY SEARCH")
    choices = [name for name, valve in valves.items() if valve.flow]

    steps = []
    total_flow = 0
    time_left = TOTAL_TIME
    last_name = START
    print(f"time: {time_left}  at valve {last_name}  total_flow={total_flow}")
    while choices and time_left:
        next_name, step_time, next_flow = "", 0, 0
        for name in choices:
            dist = valves[last_name].dist[name]
            flow = (time_left - dist - 1) * valves[name].flow
            if flow > next_flow:
                next_name, next_flow = name, flow
                step_time = dist + 1
        total_flow += next_flow
        time_left -= step_time
        choices.remove(next_name)
        print(f"time: {time_left}  opened valve {next_name}  added flow = {next_flow}  total_flow={total_flow}")
        steps.append(next_name)
        last_name = next_name

    return total_flow, steps

def sequence_score(valves: Dict[str, Valve], names: List[str]) -> int:
    total_flow = 0
    last_name = START
    time_left = TOTAL_TIME
    print(f"time: {time_left}  at valve {last_name}  total_flow={total_flow}")
    for next_name in names:
        flow = valves[next_name].flow
        dist = valves[last_name].dist[next_name]
        step_time = dist + 1
        new_flow = (time_left - step_time) * flow
        total_flow += new_flow
        time_left -= step_time
        print(f"time: {time_left}  opened valve {next_name}  added flow = {new_flow}  total_flow={total_flow}")
        last_name = next_name
    return total_flow


def optimal_search_v1(valves) -> Tuple[int, List[str]]:

    print("\n### OPTIMAL SEARCH")
    names = [name for name, valve in valves.items() if valve.flow]

    queue = [(0, TOTAL_TIME, START, [], list(names))]  # -total_flow, time_left, valve, steps
    heapify(queue)

    best_flow, best_steps = 0, []
    while queue:
        # print(f"[{len(queue)} paths queueud")
        total_flow, time_left, name, steps, choices = heappop(queue)
        # print(f"total_flow: {total_flow}, {time_left} sec left, {name}  {steps}  {choices}")
        if not choices:
            if total_flow < best_flow:
                best_flow = total_flow
                best_steps = steps
                # print(f"*** best total flow now {-total_flow}") 

        else:
            for next_name in choices:
                dist = valves[name].dist[next_name] + 1
                if dist < time_left:
                    flow = valves[next_name].flow
                    heappush(queue, (
                        total_flow - flow * (time_left - dist),
                        time_left - dist,
                        next_name,
                        steps + [next_name],
                        [name for name in choices if name != next_name]
                    ))
                else:
                    if total_flow < best_flow:
                        best_flow = total_flow
                        best_steps = steps
                        # print(f"*** best total flow now {-total_flow}") 

    return -best_flow, best_steps


@dataclass(frozen=True, order=True)
class Agent():
    name: str        # name of agent's current location 
    time_left: int   # time left 
    path: List[str]  # previously visited locations


def dfs_agent_search(valves) -> Tuple[int, List[str]]:

    print("\n### DFS AGENT SEARCH")
    names = [name for name, valve in valves.items() if valve.flow]

    # print("___ VALVES")
    # pprint(valves)

    queue = [(0, Agent(START, TOTAL_TIME, []), list(names))]  # -total_flow, agent, choices

    best_flow, best_steps = 0, []
    while queue:
        # print(f"[{len(queue)} paths queued")
        total_flow, agent, choices = queue.pop()
        # print(f"total_flow: {total_flow}, {time_left} sec left, {name}  {steps}  {choices}")
        if not choices:
            if total_flow < best_flow:
                best_flow = total_flow
                best_steps = agent.path
                print(f"*** best total flow now {-best_flow}") 

        else:
            for next_flow, next_agent, next_choices in next_steps(
                total_flow, agent, valves, choices
            ):
                if next_agent.time_left > 2:
                    queue.append((next_flow, next_agent, next_choices))
                elif next_flow < best_flow:
                    best_flow = next_flow
                    best_steps = next_agent.path
                    print(f"*** best total flow now {-best_flow}") 

    return -best_flow, best_steps


def dfs_agent_elephant_search(valves) -> Tuple[int, List[str]]:

    print("\n### DFS AGENT SEARCH")
    names = [name for name, valve in valves.items() if valve.flow]

    initial_agent = Agent(START, TOTAL_ELEPHANT_TIME, [])
    queue = [(0, initial_agent, initial_agent, list(names))]  # -total_flow, agent, choices

    best_flow, best_steps1, best_steps2 = 0, [], []
    while queue:
        # print(f"[{len(queue)} paths queued")
        total_flow, agent1, agent2, choices = queue.pop()
        # print(f"total_flow: {total_flow}, ({agent1.time_left} sec @ {agent1.name}) ({agent2.time_left} sec @ {agent2.name}) {choices}")
        if not choices:
            if total_flow < best_flow:
                best_flow = total_flow
                best_steps1 = agent1.path
                best_steps2 = agent2.path
                print(f"*** best total flow now {-best_flow}") 
                continue

        else:
            steps = next_steps(total_flow, agent1, valves, choices)
            next_agent2 = agent2
            for next_flow, next_agent, next_choices in steps:
                next_agent1 = next_agent
                if next_agent1.time_left > 2 and next_agent2.time_left > 2:
                    queue.append((next_flow, next_agent1, next_agent2, next_choices))
                    
                elif next_flow < best_flow:
                    best_flow = next_flow
                    best_steps1 = next_agent1.path
                    best_steps2 = next_agent2.path
                    print(f"*** best total flow now {-best_flow}") 

            steps = next_steps(total_flow, agent2, valves, choices)
            next_agent1 = agent1
            for next_flow, next_agent, next_choices in steps:
                next_agent2 = next_agent

                if next_agent1.time_left > 2 and next_agent2.time_left > 2:
                    queue.append((next_flow, next_agent1, next_agent2, next_choices))
                    
                elif next_flow < best_flow:
                    best_flow = next_flow
                    best_steps1 = next_agent1.path
                    best_steps2 = next_agent2.path
                    print(f"*** best total flow now {-best_flow}") 

    return -best_flow, best_steps1, best_steps2


def optimal_agent_elephant_search(valves) -> Tuple[int, List[str]]:

    print("\n### OPTIMAL AGENT SEARCH")
    names = [name for name, valve in valves.items() if valve.flow]
    # print("___ VALVES")
    # pprint(valves)

    initial_agent = Agent(START, TOTAL_ELEPHANT_TIME, [])
    queue = [(0, initial_agent, initial_agent, list(names))]  # -total_flow, agent, choices
    heapify(queue)

    best_flow, best_steps1, best_steps2 = 0, [], []
    states = 0
    while queue:
        # print(f"[{len(queue)} paths queued")
        total_flow, agent1, agent2, choices = heappop(queue)
        states += 1
        # print(f"{states:7d}) flow: {total_flow}, ({agent1.time_left} sec @ {agent1.name}) ({agent2.time_left} sec @ {agent2.name}) {agent1.path} {agent2.path} : {choices}")

        if total_flow < best_flow:
            best_flow = total_flow
            best_steps1 = agent1.path
            best_steps2 = agent2.path
            # print(f"{states:7d}) @@@ best total flow now {-best_flow}") 
            print(f"{states:7d}) @@@ best total flow now {-best_flow}") 

        if not choices:
                continue
        else:
            gap = total_flow - best_flow
            children = 0
            
            # nodes1, nodes2 = [], []
            # for name in choices:
            #     time_left1 = agent1.time_left - valves[agent1.name].dist[name] - 1
            #     time_left2 = agent2.time_left - valves[agent2.name].dist[name] - 1
            #     if time_left1 > 0:
            #         nodes1.append((valves[name].flow * time_left1, time_left1, name))
            #     if time_left2 > 0:
            #         nodes2.append((valves[name].flow * time_left2, time_left2, name))
            # nodes1.append((0, 0, ""))
            # nodes2.append((0, 0, ""))
            # nodes1.sort(reverse=True)
            # nodes2.sort(reverse=True)
            # print(f"---- gap is {gap} || {nodes1[:3]}  {nodes2[:3]}")
       
            # if nodes1[0][0] + nodes2[0][0] < gap and nodes1[0][1] < 5 and nodes2[0][1] < 5:
            #     continue

            steps = next_steps(total_flow, agent1, valves, choices)
            next_agent2 = agent2
            for next_flow, next_agent, next_choices in steps:
                next_agent1 = next_agent
                if next_agent1.time_left > 2 and next_agent2.time_left > 2:
                    heappush(queue, (next_flow, next_agent1, next_agent2, next_choices))
                    children += 1
                    
                if next_flow < best_flow:
                    best_flow = next_flow
                    best_steps1 = next_agent1.path
                    best_steps2 = next_agent2.path
                    print(f"{states:7d}) *** best total flow now {-best_flow} :: {best_steps1} :: {best_steps2}") 

            steps = next_steps(total_flow, agent2, valves, choices)
            next_agent1 = agent1
            for next_flow, next_agent, next_choices in steps:
                next_agent2 = next_agent

                if next_agent1.time_left > 2 and next_agent2.time_left > 2:
                    heappush(queue, (next_flow, next_agent1, next_agent2, next_choices))
                    children += 1
                    
                if next_flow < best_flow:
                    best_flow = next_flow
                    best_steps1 = next_agent1.path
                    best_steps2 = next_agent2.path
                    print(f"{states:7d}) *** best total flow now {-best_flow} :: {best_steps1} :: {best_steps2}") 
            # print(f"--- queued {children} new states")

    return -best_flow, best_steps1, best_steps2

def next_steps(total_flow, agent, valves, choices):
    next_steps = []
    for next_name in choices:
        dist = valves[agent.name].dist[next_name] + 1
        if dist < agent.time_left:
            flow = valves[next_name].flow
            next_flow = total_flow - flow * (agent.time_left - dist)
            step = (
                next_flow,
                Agent(next_name, agent.time_left - dist, agent.path + [next_name]),
                [name for name in choices if name != next_name]
            )
            # next_steps.append(step)
            yield step
    # next_steps.sort(reverse=True)
    # for step in next_steps:
    #     yield step


def dfs_search(valves) -> Tuple[int, List[str]]:

    print("\n### DFS SEARCH")
    names = [name for name, valve in valves.items() if valve.flow]

    queue = [(0, TOTAL_TIME, START, [], list(names))]  # -total_flow, time_left, valve, steps

    best_flow, best_steps = 0, []
    while queue:
        # print(f"[{len(queue)} paths queued")
        total_flow, time_left, name, steps, choices = queue.pop()
        # print(f"total_flow: {total_flow}, {time_left} sec left, {name}  {steps}  {choices}")
        if not choices:
            if total_flow < best_flow:
                best_flow = total_flow
                best_steps = steps
                # print(f"*** best total flow now {-total_flow}") 

        else:
            next_steps = []
            for next_name in choices:
                dist = valves[name].dist[next_name] + 1
                if dist < time_left:
                    flow = valves[next_name].flow
                    next_flow = total_flow - flow * (time_left - dist)
                    next_steps.append((
                        next_flow,
                        time_left - dist,
                        next_name,
                        steps + [next_name],
                        [name for name in choices if name != next_name]
                    ))
                else:
                    if total_flow < best_flow:
                        best_flow = total_flow
                        best_steps = steps
                        # print(f"*** best total flow now {-total_flow}") 
            next_steps.sort(reverse=True)
            queue.extend(next_steps)

    return -best_flow, best_steps


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    valves = {}
    for line in lines:
        valve = Valve.from_text(line)
        valves[valve.name] = valve
    add_distances(valves)

    total_flow, steps1, steps2 = optimal_agent_elephant_search(valves)
    return total_flow


def solve(lines: Lines) -> int:
    """Solve the problem."""
    valves = {}
    for line in lines:
        valve = Valve.from_text(line)
        valves[valve.name] = valve
    add_distances(valves)

    # print()
    # _, greedy_steps = greedy_search(valves)

    # print()
    # total_flow = sequence_score(valves, greedy_steps)

    # print()
    # optimal_steps = ["DD", "BB", "JJ", "HH", "EE", "CC"]
    # total_flow = sequence_score(valves, optimal_steps)

    # print()
    total_flow, search_steps = dfs_agent_search(valves)

    return total_flow


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
    assert result == 2181
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
    assert result == 2824
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
