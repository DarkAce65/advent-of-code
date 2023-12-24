from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import NamedTuple

from utils import get_and_cache_input

Position = tuple[int, int]


class GraphBuilderState(NamedTuple):
    from_pos: Position
    to_pos: Position
    steps: int

    def is_valid(self, problem_input: list[str]) -> bool:
        return (
            0 <= self.to_pos[0] < len(problem_input)
            and 0 <= self.to_pos[1] < len(problem_input[0])
            and problem_input[self.to_pos[0]][self.to_pos[1]] != "#"
        )


@dataclass()
class Node:
    position: Position
    neighbors: set[tuple[Position, int]]


class Destination(NamedTuple):
    position: Position
    steps: int


class Graph:
    edges: dict[Position, set[Destination]]

    def __init__(self) -> None:
        self.edges = defaultdict(set)


def build_graph(problem_input: list[str], start: Position, end: Position) -> Graph:
    graph = Graph()

    to_visit: list[tuple[Position, list[Position], bool]] = []
    to_visit.append((start, [start], False))

    while len(to_visit) > 0:
        initial_position, path, is_one_way = to_visit.pop(0)
        current = path[-1]

        if current in graph.edges and any(
            initial_position == destination.position
            for destination in graph.edges[current]
        ):
            continue

        neighbors: list[Position] = []

        neighbor = (current[0], current[1] + 1)
        if (
            neighbor[1] < len(problem_input[0])
            and problem_input[current[0]][current[1]] not in "v<^"
            and problem_input[neighbor[0]][neighbor[1]] not in "#<"
            and neighbor not in path
        ):
            neighbors.append(neighbor)
        neighbor = (current[0] + 1, current[1])
        if (
            neighbor[0] < len(problem_input)
            and problem_input[current[0]][current[1]] not in "<^>"
            and problem_input[neighbor[0]][neighbor[1]] not in "#^"
            and neighbor not in path
        ):
            neighbors.append(neighbor)
        neighbor = (current[0], current[1] - 1)
        if (
            neighbor[1] >= 0
            and problem_input[current[0]][current[1]] not in "^>v"
            and problem_input[neighbor[0]][neighbor[1]] not in "#>"
            and neighbor not in path
        ):
            neighbors.append(neighbor)
        neighbor = (current[0] - 1, current[1])
        if (
            neighbor[0] >= 0
            and problem_input[current[0]][current[1]] not in ">v<"
            and problem_input[neighbor[0]][neighbor[1]] not in "#v"
            and neighbor not in path
        ):
            neighbors.append(neighbor)

        if len(neighbors) == 1:
            new_path = path.copy()
            new_path.append(neighbors.pop())
            to_visit.append(
                (
                    initial_position,
                    new_path,
                    is_one_way or problem_input[current[0]][current[1]] in "^>v<",
                )
            )
        elif len(neighbors) > 1 or current == end:
            graph.edges[initial_position].add(Destination(current, len(path) - 1))
            if not is_one_way:
                graph.edges[path[-1]].add(Destination(initial_position, len(path) - 1))
            for neighbor in neighbors:
                to_visit.append((current, [current, neighbor], False))

    return graph


def find_longest_path(graph: Graph, start: Position, end: Position) -> int:
    to_visit: list[tuple[Position, set[Position], int]] = []
    to_visit.append((start, set([start]), 0))

    longest_path = 0

    while len(to_visit) > 0:
        current, path, steps = to_visit.pop()

        if current == end:
            longest_path = max(longest_path, steps)
            continue

        new_path = path.copy()
        new_path.add(current)

        for neighbor in graph.edges[current]:
            if neighbor.position not in new_path:
                to_visit.append((neighbor.position, new_path, steps + neighbor.steps))

    return longest_path


def part_one(problem_input: list[str]) -> int:
    start = (0, 1)
    end = (len(problem_input) - 1, len(problem_input[0]) - 2)
    graph = build_graph(problem_input, start, end)

    return find_longest_path(graph, start, end)


def part_two(problem_input: list[str]) -> int:
    start = (0, 1)
    end = (len(problem_input) - 1, len(problem_input[0]) - 2)
    input_without_slopes = [re.sub(r"[\^>v<]", ".", line) for line in problem_input]
    graph = build_graph(input_without_slopes, start, end)

    return find_longest_path(graph, start, end)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
