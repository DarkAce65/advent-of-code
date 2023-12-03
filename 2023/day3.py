from dataclasses import dataclass
from pathlib import Path


@dataclass
class Part:
    part_number: str
    is_valid: bool
    last_position: tuple[int, int]

    def __hash__(self) -> int:
        return self.last_position.__hash__()


def part_one(problem_input: list[str]) -> int:
    parts: list[Part] = []
    locations: dict[str, Part] = {}
    symbol_locations: list[tuple[int, int]] = []
    for row in range(len(problem_input)):
        for col in range(len(problem_input[row])):
            if problem_input[row][col].isnumeric():
                connected_part = parts[-1] if len(parts) > 0 else None
                if connected_part is None or connected_part.last_position != (
                    row,
                    col - 1,
                ):
                    connected_part = Part(problem_input[row][col], False, (row, col))
                    parts.append(connected_part)
                else:
                    connected_part.part_number += problem_input[row][col]
                    connected_part.last_position = (row, col)
                locations[str(row) + "-" + str(col)] = connected_part
            elif (
                not problem_input[row][col].isnumeric() and problem_input[row][col] != "."
            ):
                symbol_locations.append((row, col))

    for symbol_location in symbol_locations:
        s_row, s_col = symbol_location
        for row in range(s_row - 1, s_row + 2):
            for col in range(s_col - 1, s_col + 2):
                location_key = str(row) + "-" + str(col)
                if location_key in locations:
                    locations[location_key].is_valid = True

    return sum(int(part.part_number) for part in parts if part.is_valid)


def part_two(problem_input: list[str]) -> int:
    parts: list[Part] = []
    locations: dict[str, Part] = {}
    potential_gear_locations: list[tuple[int, int]] = []
    for row in range(len(problem_input)):
        for col in range(len(problem_input[row])):
            if problem_input[row][col].isnumeric():
                connected_part = parts[-1] if len(parts) > 0 else None
                if connected_part is None or connected_part.last_position != (
                    row,
                    col - 1,
                ):
                    connected_part = Part(problem_input[row][col], False, (row, col))
                    parts.append(connected_part)
                else:
                    connected_part.part_number += problem_input[row][col]
                    connected_part.last_position = (row, col)
                locations[str(row) + "-" + str(col)] = connected_part
            elif problem_input[row][col] == "*":
                potential_gear_locations.append((row, col))

    sum = 0
    for gear_location in potential_gear_locations:
        connected_parts: set[Part] = set()
        g_row, g_col = gear_location
        for row in range(g_row - 1, g_row + 2):
            for col in range(g_col - 1, g_col + 2):
                location_key = str(row) + "-" + str(col)
                if location_key in locations:
                    connected_parts.add(locations[location_key])
        if len(connected_parts) == 2:
            first, second = [int(p.part_number) for p in connected_parts]
            sum += first * second

    return sum


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
