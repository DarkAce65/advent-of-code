from enum import Enum
from functools import lru_cache
from typing import Literal
from utils import get_and_cache_input


Position = tuple[int, int]


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


def make_directions(tile: str, incoming_direction: Direction) -> list[Direction]:
    if tile == "|":
        if incoming_direction == Direction.RIGHT or incoming_direction == Direction.LEFT:
            return [Direction.UP, Direction.DOWN]
        else:
            return [incoming_direction]
    elif tile == "-":
        if incoming_direction == Direction.UP or incoming_direction == Direction.DOWN:
            return [Direction.RIGHT, Direction.LEFT]
        else:
            return [incoming_direction]
    elif tile == "/":
        if incoming_direction == Direction.UP:
            return [Direction.RIGHT]
        elif incoming_direction == Direction.RIGHT:
            return [Direction.UP]
        elif incoming_direction == Direction.DOWN:
            return [Direction.LEFT]
        elif incoming_direction == Direction.LEFT:
            return [Direction.DOWN]
    elif tile == "\\":
        if incoming_direction == Direction.UP:
            return [Direction.LEFT]
        elif incoming_direction == Direction.RIGHT:
            return [Direction.DOWN]
        elif incoming_direction == Direction.DOWN:
            return [Direction.RIGHT]
        elif incoming_direction == Direction.LEFT:
            return [Direction.UP]

    return [incoming_direction]


def energize_tiles(
    problem_input: list[str],
    initial_beam: tuple[Position, Direction] = ((0, 0), Direction.RIGHT),
) -> int:
    energized_tiles: set[Position] = set()

    beam_positions: set[tuple[Position, Direction]] = set()
    visited_positions: set[tuple[Position, Direction]] = set()
    beam_positions.add(initial_beam)

    while len(beam_positions) > 0:
        position, direction = beam_positions.pop()
        if (position, direction) in visited_positions:
            continue

        visited_positions.add((position, direction))
        energized_tiles.add(position)

        row, col = position
        for dir in make_directions(problem_input[row][col], direction):
            if dir == Direction.UP and row > 0:
                beam_positions.add(((row - 1, col), dir))
            elif dir == Direction.RIGHT and col < len(problem_input[row]) - 1:
                beam_positions.add(((row, col + 1), dir))
            elif dir == Direction.DOWN and row < len(problem_input) - 1:
                beam_positions.add(((row + 1, col), dir))
            elif dir == Direction.LEFT and col > 0:
                beam_positions.add(((row, col - 1), dir))

    return len(energized_tiles)


def part_one(problem_input: list[str]) -> int:
    return energize_tiles(problem_input)


def part_two(problem_input: list[str]) -> int:
    initial_beams: set[tuple[Position, Direction]] = set()

    for row in range(len(problem_input)):
        initial_beams.add(((row, 0), Direction.RIGHT))
        initial_beams.add(((row, len(problem_input[0]) - 1), Direction.LEFT))
    for col in range(len(problem_input[0])):
        initial_beams.add(((0, col), Direction.DOWN))
        initial_beams.add(((len(problem_input) - 1, col), Direction.UP))

    return max(
        energize_tiles(problem_input, initial_beam) for initial_beam in initial_beams
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
