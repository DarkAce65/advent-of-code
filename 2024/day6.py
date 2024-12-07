from bisect import bisect, insort
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import NamedTuple

from utils import get_and_cache_input


class Position(NamedTuple):
    row: int
    col: int


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def parse_map(input: list[str]) -> tuple[Position, list[Position]]:
    initial_position: Position | None = None
    obstacles: list[Position] = []

    for r, row in enumerate(input):
        for c, cell in enumerate(row):
            if cell == "^":
                initial_position = Position(r, c)
            elif cell == "#":
                obstacles.append(Position(r, c))
    assert initial_position is not None

    return (initial_position, obstacles)


def walk_map(
    initial_position: Position, dimensions: tuple[int, int], obstacles: set[Position]
) -> list[Position]:
    position = initial_position
    direction = Direction.UP
    path: list[Position] = [initial_position]

    while 0 <= position.row < dimensions[0] and 0 <= position.col < dimensions[1]:
        if path[-1] != position:
            path.append(position)

        if direction == Direction.UP:
            next_position = Position(position.row - 1, position.col)
            if next_position in obstacles:
                direction = Direction.RIGHT
            else:
                position = next_position
        elif direction == Direction.RIGHT:
            next_position = Position(position.row, position.col + 1)
            if next_position in obstacles:
                direction = Direction.DOWN
            else:
                position = next_position
        elif direction == Direction.DOWN:
            next_position = Position(position.row + 1, position.col)
            if next_position in obstacles:
                direction = Direction.LEFT
            else:
                position = next_position
        elif direction == Direction.LEFT:
            next_position = Position(position.row, position.col - 1)
            if next_position in obstacles:
                direction = Direction.UP
            else:
                position = next_position

    return path


def is_loop(
    initial_position: Position,
    obstacles_by_row: dict[int, list[int]],
    obstacles_by_col: dict[int, list[int]],
) -> int:
    current: tuple[Position, Direction] = (initial_position, Direction.UP)
    visited: set[tuple[Position, Direction]] = set()

    while True:
        if current in visited:
            return True

        visited.add(current)

        position, direction = current

        if direction == Direction.UP:
            wall_index = (
                bisect(obstacles_by_col[position.col], position.row) - 1
                if position.col in obstacles_by_col
                and len(obstacles_by_col[position.col]) > 0
                else -1
            )
            if wall_index == -1:
                return False
            current = (
                Position(obstacles_by_col[position.col][wall_index] + 1, position.col),
                Direction.RIGHT,
            )
        elif direction == Direction.RIGHT:
            wall_index = (
                bisect(obstacles_by_row[position.row], position.col)
                if position.row in obstacles_by_row
                and len(obstacles_by_row[position.row]) > 0
                else len(obstacles_by_row[position.row])
            )
            if wall_index == len(obstacles_by_row[position.row]):
                return False
            current = (
                Position(position.row, obstacles_by_row[position.row][wall_index] - 1),
                Direction.DOWN,
            )
        elif direction == Direction.DOWN:
            wall_index = (
                bisect(obstacles_by_col[position.col], position.row)
                if position.col in obstacles_by_col
                and len(obstacles_by_col[position.col]) > 0
                else len(obstacles_by_col[position.col])
            )
            if wall_index == len(obstacles_by_col[position.col]):
                return False
            current = (
                Position(obstacles_by_col[position.col][wall_index] - 1, position.col),
                Direction.LEFT,
            )
        elif direction == Direction.LEFT:
            wall_index = (
                bisect(obstacles_by_row[position.row], position.col) - 1
                if position.row in obstacles_by_row
                and len(obstacles_by_row[position.row]) > 0
                else -1
            )
            if wall_index == -1:
                return False
            current = (
                Position(position.row, obstacles_by_row[position.row][wall_index] + 1),
                Direction.UP,
            )


def part_one(problem_input: list[str]) -> int:
    initial_position, obstacles = parse_map(problem_input)

    path = walk_map(
        initial_position,
        (len(problem_input), len(problem_input[0])),
        set(obstacles),
    )

    return len(set(path))


def part_two(problem_input: list[str]) -> int:
    initial_position, obstacles = parse_map(problem_input)

    obstacles_by_row: dict[int, list[int]] = defaultdict(list)
    obstacles_by_col: dict[int, list[int]] = defaultdict(list)

    for obstacle in obstacles:
        obstacles_by_row[obstacle.row].append(obstacle.col)
        obstacles_by_col[obstacle.col].append(obstacle.row)

    path = walk_map(
        initial_position,
        (len(problem_input), len(problem_input[0])),
        set(obstacles),
    )

    sum = 0
    for potential_obstacle in set(path[1:]):
        o_by_row = deepcopy(obstacles_by_row)
        o_by_col = deepcopy(obstacles_by_col)

        insort(o_by_row[potential_obstacle.row], potential_obstacle.col)
        insort(o_by_col[potential_obstacle.col], potential_obstacle.row)
        if is_loop(initial_position, o_by_row, o_by_col):
            sum += 1
    return sum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
