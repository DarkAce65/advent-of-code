import copy
import math
from pathlib import Path
from typing import Optional, TypedDict


def is_low_point(heightmap: list[list[int]], row: int, col: int) -> bool:
    height = heightmap[row][col]
    if row > 0 and heightmap[row - 1][col] <= height:
        return False
    elif row < len(heightmap) - 1 and heightmap[row + 1][col] <= height:
        return False
    elif col > 0 and heightmap[row][col - 1] <= height:
        return False
    elif col < len(heightmap[row]) - 1 and heightmap[row][col + 1] <= height:
        return False

    return True


def part_one(heightmap: list[list[int]]) -> int:
    risk = 0
    for row in range(len(heightmap)):
        for col in range(len(heightmap[row])):
            if is_low_point(heightmap, row, col):
                risk += heightmap[row][col] + 1

    return risk


class Location(TypedDict):
    height: int
    group: Optional[int]


def fill_basin(heightmap: list[list[int]], row: int, col: int) -> int:
    filled_locations = 0

    heightmap[row][col] = 9
    filled_locations += 1

    if row > 0 and heightmap[row - 1][col] < 9:
        filled_locations += fill_basin(heightmap, row - 1, col)
    if row < len(heightmap) - 1 and heightmap[row + 1][col] < 9:
        filled_locations += fill_basin(heightmap, row + 1, col)
    if col > 0 and heightmap[row][col - 1] < 9:
        filled_locations += fill_basin(heightmap, row, col - 1)
    if col < len(heightmap[row]) - 1 and heightmap[row][col + 1] < 9:
        filled_locations += fill_basin(heightmap, row, col + 1)

    return filled_locations


def part_two(heightmap: list[list[int]]) -> int:
    modifiable_heightmap = copy.deepcopy(heightmap)

    basins: list[int] = []
    for row in range(len(modifiable_heightmap)):
        for col in range(len(modifiable_heightmap[row])):
            if modifiable_heightmap[row][col] < 9:
                basins.append(fill_basin(modifiable_heightmap, row, col))

    return math.prod(sorted(basins, reverse=True)[:3])


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    heightmap = [list(map(int, row)) for row in problem_input]

    print("Part One: ", part_one(heightmap))
    print("Part Two: ", part_two(heightmap))
