from dataclasses import dataclass

from utils import get_and_cache_input


@dataclass
class Part:
    part_number: str
    last_position: tuple[int, int]

    def __hash__(self) -> int:
        return self.last_position.__hash__()


def build_parts_list(schematic: list[str]) -> tuple[list[Part], dict[str, Part]]:
    parts: list[Part] = []
    part_locations: dict[str, Part] = {}
    for row in range(len(schematic)):
        for col in range(len(schematic[row])):
            if schematic[row][col].isnumeric():
                connected_part = parts[-1] if len(parts) > 0 else None
                if connected_part is None or connected_part.last_position != (
                    row,
                    col - 1,
                ):
                    connected_part = Part(schematic[row][col], (row, col))
                    parts.append(connected_part)
                else:
                    connected_part.part_number += schematic[row][col]
                    connected_part.last_position = (row, col)
                part_locations[str(row) + "-" + str(col)] = connected_part

    return (parts, part_locations)


def part_one(problem_input: list[str]) -> int:
    _, part_locations = build_parts_list(problem_input)

    valid_parts: set[Part] = set()
    for row in range(len(problem_input)):
        for col in range(len(problem_input[row])):
            if not problem_input[row][col].isnumeric() and problem_input[row][col] != ".":
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        location_key = str(r) + "-" + str(c)
                        if location_key in part_locations:
                            valid_parts.add(part_locations[location_key])

    return sum(int(part.part_number) for part in valid_parts)


def part_two(problem_input: list[str]) -> int:
    _, part_locations = build_parts_list(problem_input)

    sum = 0
    for row in range(len(problem_input)):
        for col in range(len(problem_input[row])):
            if problem_input[row][col] == "*":
                connected_parts: set[Part] = set()
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        location_key = str(r) + "-" + str(c)
                        if location_key in part_locations:
                            connected_parts.add(part_locations[location_key])
                if len(connected_parts) == 2:
                    first, second = [int(p.part_number) for p in connected_parts]
                    sum += first * second

    return sum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
