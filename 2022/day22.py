from __future__ import annotations

import re

from utils import get_and_cache_input

Position = tuple[int, int]


# def parse_map(
#     rows: list[str], map_width: int
# ) -> tuple[
#     Position,
#     dict[int, tuple[bool, list[tuple[int, int]]]],
#     dict[int, tuple[bool, list[tuple[int, int]]]],
# ]:
#     start_cell: Position = (0, 0)
#     row_spans: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
#     col_spans: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
#     for row_index in range(len(rows)):
#         row = row_index + 1
#         for col_index in range(len(rows[row_index])):
#             col = col_index + 1
#             if rows[row_index][col_index] == ".":
#                 if row == 1 and start_cell == (0, 0):
#                     start_cell = (col, 1)
#                 if len(row_spans[row]) == 0 or row_spans[row][-1][1] < col - 1:
#                     row_spans[row].append((col, col))
#                 else:
#                     row_spans[row][-1] = (row_spans[row][-1][0], col)

#     row_bounds: dict[int, tuple[bool, list[tuple[int, int]]]] = {}
#     for row in row_spans.keys():
#         row_bounds[row] = (row_can_wrap[row], row_spans[row])
#     col_bounds: dict[int, tuple[bool, list[tuple[int, int]]]] = {}
#     for col in col_spans.keys():
#         col_bounds[col] = (col_can_wrap[col], col_spans[col])
#     return (start_cell, row_bounds, col_bounds)


def parse_map(
    rows: list[str], map_width: int
) -> tuple[
    Position, dict[Position, bool], dict[int, tuple[int, int]], dict[int, tuple[int, int]]
]:
    start_cell: Position = (0, 0)
    cells: dict[Position, bool] = {}
    row_bounds: dict[int, tuple[int, int]] = {}
    col_bounds: dict[int, tuple[int, int]] = {}

    for row_index in range(len(rows)):
        row = row_index + 1
        for col_index in range(len(rows[row_index])):
            col = col_index + 1

            if row == 1 and start_cell == (0, 0) and rows[row_index][col_index] == ".":
                start_cell = (row, col)

            if rows[row_index][col_index] == ".":
                cells[(row, col)] = True
            elif rows[row_index][col_index] == "#":
                cells[(row, col)] = False

    for row in range(1, len(rows) + 1):
        row_bounds[row] = (
            min(position[1] for position in cells.keys() if position[0] == row),
            max(position[1] for position in cells.keys() if position[0] == row),
        )
    for col in range(1, map_width + 1):
        col_bounds[col] = (
            min(position[0] for position in cells.keys() if position[1] == col),
            max(position[0] for position in cells.keys() if position[1] == col),
        )

    return (start_cell, cells, row_bounds, col_bounds)


def parse_path(path: str) -> list[int | str]:
    parsed_path = re.split(r"([RL])", path)
    return [int(action) if action.isdigit() else str(action) for action in parsed_path]


def part_one(problem_input: list[str]) -> int:
    map_input: list[str] = []
    map_width = 0
    path: str = ""
    is_map = True
    for line in problem_input:
        if len(line) == 0:
            is_map = False
            continue

        if is_map:
            map_input.append(line)
            if map_width < len(line):
                map_width = len(line)
        else:
            path = line

    start, cells, row_bounds, col_bounds = parse_map(map_input, map_width)
    parsed_path = parse_path(path)

    position = start
    facing = 0
    for action in parsed_path:
        if isinstance(action, int):
            row_low, row_high = row_bounds[position[0]]
            col_low, col_high = col_bounds[position[1]]
            steps = 0
            d_row = 0
            d_col = 0
            if facing == 0:
                d_col = 1
            elif facing == 1:
                d_row = 1
            elif facing == 2:
                d_col = -1
            elif facing == 3:
                d_row = -1
            while steps < action:
                new_row = position[0] + d_row
                new_col = position[1] + d_col
                if new_col < row_low:
                    new_col = row_high
                elif row_high < new_col:
                    new_col = row_low
                if new_row < col_low:
                    new_row = col_high
                elif col_high < new_row:
                    new_row = col_low

                if not cells[(new_row, new_col)]:
                    break

                position = (new_row, new_col)
                steps += 1
        else:
            if action == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4

    return 1000 * position[0] + 4 * position[1] + facing


def part_two(problem_input: list[str]) -> int:
    map_input: list[str] = []
    map_width = 0
    path: str = ""
    is_map = True
    for line in problem_input:
        if len(line) == 0:
            is_map = False
            continue

        if is_map:
            map_input.append(line)
            if map_width < len(line):
                map_width = len(line)
        else:
            path = line

    start, cells, row_bounds, col_bounds = parse_map(map_input, map_width)
    parsed_path = parse_path(path)

    position = start
    facing = 0
    for action in parsed_path:
        if isinstance(action, int):
            steps = 0
            while steps < action:
                row_low, row_high = row_bounds[position[0]]
                col_low, col_high = col_bounds[position[1]]
                d_row = 0
                d_col = 0
                if facing == 0:
                    d_col = 1
                elif facing == 1:
                    d_row = 1
                elif facing == 2:
                    d_col = -1
                elif facing == 3:
                    d_row = -1
                new_row = position[0] + d_row
                new_col = position[1] + d_col
                new_facing = facing

                if 1 <= position[0] <= 50 and new_col < row_low:
                    new_row = 151 + (-position[0])
                    new_col = 1
                    new_facing = 0
                elif 1 <= position[0] <= 50 and row_high < new_col:
                    new_row = 151 + (-position[0])
                    new_col = 100
                    new_facing = 2
                elif 51 <= position[0] <= 100 and new_col < row_low:
                    new_row = 101
                    new_col = position[0] - 50
                    new_facing = 1
                elif 51 <= position[0] <= 100 and row_high < new_col:
                    new_row = 50
                    new_col = 100 + (position[0] - 50)
                    new_facing = 3
                elif 101 <= position[0] <= 150 and new_col < row_low:
                    new_row = 151 - position[0]
                    new_col = 51
                    new_facing = 0
                elif 101 <= position[0] <= 150 and row_high < new_col:
                    new_row = 151 - position[0]
                    new_col = 150
                    new_facing = 2
                elif 151 <= position[0] <= 200 and new_col < row_low:
                    new_row = 1
                    new_col = 50 + (position[0] - 150)
                    new_facing = 1
                elif 151 <= position[0] <= 200 and row_high < new_col:
                    new_row = 150
                    new_col = 50 + (position[0] - 150)
                    new_facing = 3
                elif 1 <= position[1] <= 50 and new_row < col_low:
                    new_row = 50 + position[1]
                    new_col = 51
                    new_facing = 0
                elif 1 <= position[1] <= 50 and col_high < new_row:
                    new_row = 1
                    new_col = 100 + position[1]
                    new_facing = 1
                elif 51 <= position[1] <= 100 and new_row < col_low:
                    new_row = 150 + (position[1] - 50)
                    new_col = 1
                    new_facing = 0
                elif 51 <= position[1] <= 100 and col_high < new_row:
                    new_row = 150 + (position[1] - 50)
                    new_col = 50
                    new_facing = 2
                elif 101 <= position[1] <= 150 and new_row < col_low:
                    new_row = 200
                    new_col = position[1] - 100
                    new_facing = 3
                elif 101 <= position[1] <= 150 and col_high < new_row:
                    new_row = 50 + (position[1] - 100)
                    new_col = 100
                    new_facing = 2

                if not cells[(new_row, new_col)]:
                    break

                position = (new_row, new_col)
                facing = new_facing
                steps += 1
        else:
            if action == "R":
                facing = (facing + 1) % 4
            else:
                facing = (facing - 1) % 4

    return 1000 * position[0] + 4 * position[1] + facing


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
