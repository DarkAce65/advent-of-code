import re

from utils import get_and_cache_input


def compute_size(instructions: list[tuple[str, int]]) -> int:
    filled_tiles = 1
    width = 0
    for direction, distance in instructions:
        if direction == "U":
            filled_tiles -= (width - 1) * distance
        elif direction == "R":
            width += distance
            filled_tiles += distance
        elif direction == "D":
            filled_tiles += width * distance
        elif direction == "L":
            width -= distance

    return filled_tiles


def part_one(problem_input: list[str]) -> int:
    instructions: list[tuple[str, int]] = []
    for line in problem_input:
        match = re.match(r"([URDL]) (\d+) \(#[0-9a-f]{6}\)", line)
        assert match is not None

        direction = match.group(1)
        distance = int(match.group(2))
        instructions.append((direction, distance))

    return compute_size(instructions)


def part_two(problem_input: list[str]) -> int:
    instructions: list[tuple[str, int]] = []
    for line in problem_input:
        match = re.match(r"[URDL] \d+ \(#([0-9a-f]{6})\)", line)
        assert match is not None

        color = match.group(1)
        if color[5] == "0":
            direction = "R"
        if color[5] == "1":
            direction = "D"
        if color[5] == "2":
            direction = "L"
        if color[5] == "3":
            direction = "U"
        distance = int(color[:5], 16)
        instructions.append((direction, distance))

    return compute_size(instructions)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
