from enum import Enum
from typing import NamedTuple

from utils import get_and_cache_input


class Position(NamedTuple):
    row: int
    col: int


class Direction(Enum):
    NORTH = (-1, 0)
    NORTH_EAST = (-1, 1)
    EAST = (0, 1)
    SOUTH_EAST = (1, 1)
    SOUTH = (1, 0)
    SOUTH_WEST = (1, -1)
    WEST = (0, -1)
    NORTH_WEST = (-1, -1)


def has_xmas(input: list[str], position: Position, direction: Direction) -> bool:
    current_position = position
    for c in "XMAS":
        if (current_position.row < 0 or current_position.row >= len(input)) or (
            current_position.col < 0
            or current_position.col >= len(input[current_position.row])
        ):
            return False
        if input[current_position.row][current_position.col] != c:
            return False
        current_position = Position(
            current_position.row + direction.value[0],
            current_position.col + direction.value[1],
        )

    return True


def has_x_mas(input: list[str], position: Position) -> bool:
    if (
        position.row <= 0
        or position.row >= len(input) - 1
        or position.col <= 0
        or position.col >= len(input[position.row]) - 1
    ):
        return False

    north_east = Position(position.row - 1, position.col + 1)
    south_east = Position(position.row + 1, position.col + 1)
    south_west = Position(position.row + 1, position.col - 1)
    north_west = Position(position.row - 1, position.col - 1)

    corners = (
        input[north_east.row][north_east.col]
        + input[south_east.row][south_east.col]
        + input[south_west.row][south_west.col]
        + input[north_west.row][north_west.col]
    )
    return (
        corners == "MMSS" or corners == "SMMS" or corners == "SSMM" or corners == "MSSM"
    )


def part_one(problem_input: list[str]) -> int:
    sum = 0
    for r, row in enumerate(problem_input):
        for c, char in enumerate(row):
            if char == "X":
                for direction in Direction:
                    if has_xmas(problem_input, Position(r, c), direction):
                        sum += 1
    return sum


def part_two(problem_input: list[str]) -> int:
    sum = 0
    for r, row in enumerate(problem_input):
        for c, char in enumerate(row):
            if char == "A":
                if has_x_mas(problem_input, Position(r, c)):
                    sum += 1
    return sum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
