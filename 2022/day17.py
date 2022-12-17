import functools
import time
from collections import defaultdict
from pathlib import Path

ROCK_PATTERNS = [
    ["####"],
    [".#.", "###", ".#."],
    ["..#", "..#", "###"],
    ["#", "#", "#", "#"],
    ["##", "##"],
]
TOWER_WIDTH = 7


Position = tuple[int, int]


def get_rock_coordinates(rock: list[str]) -> set[Position]:
    rock_coordinates: set[Position] = set()
    for i, row in enumerate(rock):
        for j, c in enumerate(row):
            if c == "#":
                rock_coordinates.add((j, len(rock) - i - 1))

    return rock_coordinates


ROCK_COORDINATES = [get_rock_coordinates(rock_pattern) for rock_pattern in ROCK_PATTERNS]
ROCK_WIDTHS = [len(rock_pattern[0]) for rock_pattern in ROCK_PATTERNS]


def can_rock_move_left(
    rock_coordinates: set[Position], x: int, y: int, existing_rock: set[Position]
) -> bool:
    if x <= 0:
        return False

    for rx, ry in rock_coordinates:
        if ((x - 1) + rx, y + ry) in existing_rock:
            return False

    return True


def can_rock_move_right(
    rock_coordinates: set[Position],
    x: int,
    y: int,
    existing_rock: set[Position],
    rock_width: int,
) -> bool:
    if x + rock_width >= TOWER_WIDTH:
        return False

    for rx, ry in rock_coordinates:
        if ((x + 1) + rx, y + ry) in existing_rock:
            return False

    return True


def can_rock_move_down(
    rock_coordinates: set[Position], x: int, y: int, existing_rock: set[Position]
) -> bool:
    if y <= 0:
        return False

    for rx, ry in rock_coordinates:
        if (x + rx, (y - 1) + ry) in existing_rock:
            return False

    return True


def print_tower(existing_rock: set[Position], tower_height: int):
    for y in range(tower_height + 2, -1, -1):
        line = "|"
        for x in range(7):
            if (x, y) in existing_rock:
                line += "#"
            else:
                line += "."
        line += "|"
        print(line)
    print("---------")


def find_height_path_to_right(
    x: int, y: int, existing_rock: set[Position]
) -> list[int] | None:
    if x == 6:
        return [y]
    for dy in range(1, -2, -1):
        if (x + 1, y + dy) in existing_rock:
            path = find_height_path_to_right(x + 1, y + dy, existing_rock)
            if path is not None:
                path.insert(0, y + dy)
                return path

    return None


def prune_rocks(existing_rock: set[Position]) -> tuple[set[Position], int]:
    try:
        max_left = max(y for x, y in existing_rock if x == 0)
    except ValueError:
        return (existing_rock, 0)
    heights = find_height_path_to_right(0, max_left, existing_rock)
    if heights is None:
        return (existing_rock, 0)

    heights.insert(0, max_left)
    offset = min(heights)
    return ({(x, y - offset) for x, y in existing_rock if y >= heights[x]}, offset)


def part_one(problem_input: list[str]) -> int:
    jet_pattern = problem_input[0]
    jet_index = 0

    tower_height = 0
    tower_height_offset = 0
    existing_rock: set[Position] = set()
    for i in range(2022):
        if i % 10 == 0:
            existing_rock, offset = prune_rocks(existing_rock)
            tower_height_offset += offset
            tower_height -= offset
        rock_index = i % len(ROCK_PATTERNS)
        rock_coordinates = ROCK_COORDINATES[rock_index]
        x, y = 2, tower_height + 3

        falling = False
        while True:
            if falling:
                if not can_rock_move_down(rock_coordinates, x, y, existing_rock):
                    break
                y -= 1
                falling = False
            else:
                jet_direction = jet_pattern[jet_index]
                if jet_direction == "<" and can_rock_move_left(
                    rock_coordinates, x, y, existing_rock
                ):
                    x -= 1
                elif jet_direction == ">" and can_rock_move_right(
                    rock_coordinates, x, y, existing_rock, ROCK_WIDTHS[rock_index]
                ):
                    x += 1

                jet_index = (jet_index + 1) % len(jet_pattern)
                falling = True

        rock_world_coordinates = {(x + rx, y + ry) for rx, ry in rock_coordinates}
        existing_rock = existing_rock.union(rock_world_coordinates)
        tower_height = max(tower_height, max(y + 1 for _, y in rock_world_coordinates))

    return tower_height + tower_height_offset


def part_two(problem_input: list[str]) -> int:
    jet_pattern = problem_input[0]
    jet_index = 0

    cache: dict[tuple[frozenset[Position], int, int], tuple[int, int]] = {}

    tower_height = 0
    tower_height_offset = 0
    existing_rock: set[Position] = set()
    i = 0
    while i < 1_000_000_000_000:
        rock_index = i % len(ROCK_PATTERNS)
        if (frozenset(existing_rock), jet_index, rock_index) in cache:
            prev_rock_index, prev_height = cache[
                (frozenset(existing_rock), jet_index, rock_index)
            ]
            multiplier = max(1, int((1_000_000_000_000 - i) / (i - prev_rock_index)))
            if i + (i - prev_rock_index) * multiplier < 1_000_000_000_000:
                cache[(frozenset(existing_rock), jet_index, rock_index)] = (
                    i,
                    tower_height + tower_height_offset,
                )
                i += (i - prev_rock_index) * multiplier
                tower_height_offset += (
                    tower_height + tower_height_offset - prev_height
                ) * multiplier
                continue
        if i % 10 == 0:
            existing_rock, offset = prune_rocks(existing_rock)
            tower_height_offset += offset
            tower_height -= offset
            if offset > 0:
                cache[(frozenset(existing_rock), jet_index, rock_index)] = (
                    i,
                    tower_height + tower_height_offset,
                )
        rock_coordinates = ROCK_COORDINATES[rock_index]
        x, y = 2, tower_height + 3

        falling = False
        while True:
            if falling:
                if not can_rock_move_down(rock_coordinates, x, y, existing_rock):
                    break
                y -= 1
                falling = False
            else:
                jet_direction = jet_pattern[jet_index]
                if jet_direction == "<" and can_rock_move_left(
                    rock_coordinates, x, y, existing_rock
                ):
                    x -= 1
                elif jet_direction == ">" and can_rock_move_right(
                    rock_coordinates, x, y, existing_rock, ROCK_WIDTHS[rock_index]
                ):
                    x += 1

                jet_index = (jet_index + 1) % len(jet_pattern)
                falling = True

        rock_world_coordinates = {(x + rx, y + ry) for rx, ry in rock_coordinates}
        existing_rock = existing_rock.union(rock_world_coordinates)
        tower_height = max(tower_height, max(y + 1 for _, y in rock_world_coordinates))
        i += 1

    return tower_height + tower_height_offset


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
