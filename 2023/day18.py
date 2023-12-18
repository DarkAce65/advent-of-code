import re
from typing import Literal

from utils import get_and_cache_input

Position = tuple[int, int]


def part_one(problem_input: list[str]) -> int:
    walls: dict[
        Position, Literal["horizontal", "vertical", "corner_up", "corner_down"]
    ] = {}

    position: Position = (0, 0)
    min_max_row = (0, 0)
    min_max_col = (0, 0)
    for line in problem_input:
        match = re.match(r"([URDL]) (\d+) \(#[0-9a-f]{6}\)", line)
        assert match is not None

        direction, distance = match.group(1), int(match.group(2))
        if direction == "U":
            walls[position] = "corner_up"
            for d in range(distance):
                walls[(position[0] - d - 1, position[1])] = "vertical"
            position = (position[0] - distance, position[1])
            walls[position] = "corner_down"
        elif direction == "R":
            for d in range(distance):
                walls[(position[0], position[1] + d + 1)] = "horizontal"
            position = (position[0], position[1] + distance)
        elif direction == "D":
            walls[position] = "corner_down"
            for d in range(distance):
                walls[(position[0] + d + 1, position[1])] = "vertical"
            position = (position[0] + distance, position[1])
            walls[position] = "corner_up"
        elif direction == "L":
            for d in range(distance):
                walls[(position[0], position[1] - d - 1)] = "horizontal"
            position = (position[0], position[1] - distance)

        min_max_row = (min(min_max_row[0], position[0]), max(min_max_row[1], position[0]))
        min_max_col = (min(min_max_col[0], position[1]), max(min_max_col[1], position[1]))

    filled_tiles = 0
    for row in range(min_max_row[0], min_max_row[1] + 1):
        is_inside = False
        found_up = False
        found_down = False
        for col in range(min_max_col[0], min_max_col[1] + 1):
            if (row, col) in walls:
                if walls[(row, col)] == "corner_up":
                    found_up = not found_up
                elif walls[(row, col)] == "corner_down":
                    found_down = not found_down
                elif walls[(row, col)] == "vertical":
                    is_inside = not is_inside

                if found_up and found_down:
                    is_inside = not is_inside
                    found_up = False
                    found_down = False

                filled_tiles += 1
            elif is_inside:
                filled_tiles += 1

    return filled_tiles


directions = {"0": "R", "1": "D", "2": "L", "3": "U"}


def part_two(problem_input: list[str]) -> int:
    filled_tiles = 0
    width = 0
    for line in problem_input:
        match = re.match(r"[URDL] \d+ \(#([0-9a-f]{6})\)", line)
        assert match is not None

        color = match.group(1)
        direction = directions[color[5]]
        distance = int(color[:5], 16)

        if direction == "U":
            filled_tiles -= (width - 1) * distance
        elif direction == "R":
            width += distance
            filled_tiles += distance
        elif direction == "D":
            filled_tiles += width * distance
        elif direction == "L":
            width -= distance

    return filled_tiles + 1


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
