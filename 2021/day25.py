from __future__ import annotations

import copy
from enum import Enum, unique

from utils import get_and_cache_input


@unique
class Space(str, Enum):
    EMPTY = "EMPTY"
    EAST = "EAST"
    SOUTH = "SOUTH"

    def from_input(space: str) -> Space:
        if space == ".":
            return Space.EMPTY
        elif space == ">":
            return Space.EAST
        elif space == "v":
            return Space.SOUTH

        raise ValueError(f"Unknown space value: {space}")

    def __repr__(self) -> str:
        if self == Space.EMPTY:
            return "."
        if self == Space.EAST:
            return ">"
        if self == Space.SOUTH:
            return "v"

        raise ValueError(f"Unknown space value: {self}")


def parse_sea_floor(problem_input: list[str]) -> list[list[Space]]:
    sea_floor = []
    for line in problem_input:
        row = []
        for space in line:
            row.append(Space.from_input(space))
        sea_floor.append(row)

    return sea_floor


def part_one(sea_floor: list[list[Space]]) -> int:
    step = 0
    width = len(sea_floor[0])
    height = len(sea_floor)
    while True:
        step += 1
        locations_to_move: set[tuple[int, int]] = set()
        for row in range(height):
            for col in range(width):
                space = sea_floor[row][col]
                if space == Space.EMPTY:
                    continue

                if space == Space.EAST:
                    if sea_floor[row][(col + 1) % width] == Space.EMPTY:
                        locations_to_move.add((row, col))
                elif space == Space.SOUTH:
                    if (
                        sea_floor[(row + 1) % height][col] == Space.EMPTY
                        and sea_floor[(row + 1) % height][(col - 1 + width) % width]
                        != Space.EAST
                    ) or (
                        sea_floor[(row + 1) % height][col] == Space.EAST
                        and sea_floor[(row + 1) % height][(col + 1) % width]
                        == Space.EMPTY
                    ):
                        locations_to_move.add((row, col))

        if len(locations_to_move) == 0:
            break

        next_sea_floor = copy.deepcopy(sea_floor)
        for row, col in locations_to_move:
            space = sea_floor[row][col]
            if space == Space.EAST:
                if space == next_sea_floor[row][col]:
                    next_sea_floor[row][col] = Space.EMPTY
                next_sea_floor[row][(col + 1) % width] = Space.EAST
            elif space == Space.SOUTH:
                if space == next_sea_floor[row][col]:
                    next_sea_floor[row][col] = Space.EMPTY
                next_sea_floor[(row + 1) % height][col] = Space.SOUTH

        sea_floor = next_sea_floor

    return step


def part_two(problem_input: list[str]) -> int:
    pass


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    sea_floor = parse_sea_floor(problem_input)

    print("Part One: ", part_one(sea_floor))
    print("Part Two: ", part_two(problem_input))
