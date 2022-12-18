from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Literal, Union

Position = tuple[int, int, int]
Direction = Union[
    Literal["+x"],
    Literal["-x"],
    Literal["+y"],
    Literal["-y"],
    Literal["+z"],
    Literal["-z"],
]


def get_prioritized_neighbors(
    position: Position, priority_direction: Direction
) -> deque[Position]:
    neighbors: deque[Position] = deque()
    x, y, z = position
    if priority_direction == "+x":
        neighbors.append((x + 1, y, z))
        neighbors.append((x, y + 1, z))
        neighbors.append((x, y - 1, z))
        neighbors.append((x, y, z + 1))
        neighbors.append((x, y, z - 1))
        neighbors.append((x - 1, y, z))
    elif priority_direction == "-x":
        neighbors.append((x - 1, y, z))
        neighbors.append((x, y + 1, z))
        neighbors.append((x, y - 1, z))
        neighbors.append((x, y, z + 1))
        neighbors.append((x, y, z - 1))
        neighbors.append((x + 1, y, z))
    elif priority_direction == "+y":
        neighbors.append((x, y + 1, z))
        neighbors.append((x + 1, y, z))
        neighbors.append((x - 1, y, z))
        neighbors.append((x, y, z + 1))
        neighbors.append((x, y, z - 1))
        neighbors.append((x, y - 1, z))
    elif priority_direction == "-y":
        neighbors.append((x, y - 1, z))
        neighbors.append((x + 1, y, z))
        neighbors.append((x - 1, y, z))
        neighbors.append((x, y, z + 1))
        neighbors.append((x, y, z - 1))
        neighbors.append((x, y + 1, z))
    elif priority_direction == "+z":
        neighbors.append((x, y, z + 1))
        neighbors.append((x + 1, y, z))
        neighbors.append((x - 1, y, z))
        neighbors.append((x, y + 1, z))
        neighbors.append((x, y - 1, z))
        neighbors.append((x, y, z - 1))
    elif priority_direction == "-z":
        neighbors.append((x, y, z - 1))
        neighbors.append((x + 1, y, z))
        neighbors.append((x - 1, y, z))
        neighbors.append((x, y + 1, z))
        neighbors.append((x, y - 1, z))
        neighbors.append((x, y, z + 1))
    return neighbors


def can_reach_boundary(
    priority_direction: Direction,
    bounds: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    occupied_spaces: set[Position],
    exposed_spaces: set[Position],
    start: Position,
) -> tuple[bool, set[Position]]:
    nodes_to_visit: deque[Position] = deque()
    nodes_to_visit.append(start)
    visited_nodes: set[Position] = set()
    while len(nodes_to_visit) > 0:
        node = nodes_to_visit.popleft()

        if node in occupied_spaces:
            continue
        elif node in exposed_spaces:
            return (True, visited_nodes)

        x, y, z = node
        (x_low, x_high), (y_low, y_high), (z_low, z_high) = bounds
        if (
            x == x_low - 1
            or x == x_high + 1
            or y == y_low - 1
            or y == y_high + 1
            or z == z_low - 1
            or z == z_high + 1
        ):
            return (True, visited_nodes)

        visited_nodes.add(node)

        nodes_to_visit.extendleft(
            neighbor
            for neighbor in get_prioritized_neighbors(node, priority_direction)
            if neighbor not in occupied_spaces and neighbor not in visited_nodes
        )

    return (False, visited_nodes)


def part_one(problem_input: list[str]) -> int:
    cubes: set[Position] = set()
    for line in problem_input:
        x, y, z = [int(n) for n in line.split(",")]
        cubes.add((x, y, z))

    surface_area = 0
    for x, y, z in cubes:
        if (x + 1, y, z) not in cubes:
            surface_area += 1
        if (x - 1, y, z) not in cubes:
            surface_area += 1
        if (x, y + 1, z) not in cubes:
            surface_area += 1
        if (x, y - 1, z) not in cubes:
            surface_area += 1
        if (x, y, z + 1) not in cubes:
            surface_area += 1
        if (x, y, z - 1) not in cubes:
            surface_area += 1

    return surface_area


def part_two(problem_input: list[str]) -> int:
    cubes: set[Position] = set()
    x_bounds = (0, 0)
    y_bounds = (0, 0)
    z_bounds = (0, 0)
    for i, line in enumerate(problem_input):
        x, y, z = [int(n) for n in line.split(",")]
        cubes.add((x, y, z))

        if i == 0:
            x_bounds = (x, x)
            y_bounds = (y, y)
            z_bounds = (z, z)
        else:
            if x < x_bounds[0]:
                x_bounds = (x, x_bounds[1])
            elif x_bounds[1] < x:
                x_bounds = (x_bounds[0], x)
            if y < y_bounds[0]:
                y_bounds = (y, y_bounds[1])
            elif y_bounds[1] < y:
                y_bounds = (y_bounds[0], y)
            if z < z_bounds[0]:
                z_bounds = (z, z_bounds[1])
            elif z_bounds[1] < z:
                z_bounds = (z_bounds[0], z)

    bounds = (x_bounds, y_bounds, z_bounds)
    surface_area = 0
    filled_cubes = cubes.copy()
    exposed_cubes: set[Position] = set()
    for x, y, z in cubes:
        is_exposed, visited_cubes = can_reach_boundary(
            "+x", bounds, filled_cubes, exposed_cubes, (x + 1, y, z)
        )
        if is_exposed:
            surface_area += 1
            exposed_cubes = exposed_cubes.union(visited_cubes)
        else:
            filled_cubes = filled_cubes.union(visited_cubes)
        is_exposed, visited_cubes = can_reach_boundary(
            "-x", bounds, filled_cubes, exposed_cubes, (x - 1, y, z)
        )
        if is_exposed:
            surface_area += 1
            exposed_cubes = exposed_cubes.union(visited_cubes)
        else:
            filled_cubes = filled_cubes.union(visited_cubes)
        is_exposed, visited_cubes = can_reach_boundary(
            "+y", bounds, filled_cubes, exposed_cubes, (x, y + 1, z)
        )
        if is_exposed:
            surface_area += 1
            exposed_cubes = exposed_cubes.union(visited_cubes)
        else:
            filled_cubes = filled_cubes.union(visited_cubes)
        is_exposed, visited_cubes = can_reach_boundary(
            "-y", bounds, filled_cubes, exposed_cubes, (x, y - 1, z)
        )
        if is_exposed:
            surface_area += 1
            exposed_cubes = exposed_cubes.union(visited_cubes)
        else:
            filled_cubes = filled_cubes.union(visited_cubes)
        is_exposed, visited_cubes = can_reach_boundary(
            "+z", bounds, filled_cubes, exposed_cubes, (x, y, z + 1)
        )
        if is_exposed:
            surface_area += 1
            exposed_cubes = exposed_cubes.union(visited_cubes)
        else:
            filled_cubes = filled_cubes.union(visited_cubes)
        is_exposed, visited_cubes = can_reach_boundary(
            "-z", bounds, filled_cubes, exposed_cubes, (x, y, z - 1)
        )
        if is_exposed:
            surface_area += 1
        elif visited_cubes is not None:
            filled_cubes = filled_cubes.union(visited_cubes)

    return surface_area


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
