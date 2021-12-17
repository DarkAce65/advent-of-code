from dataclasses import dataclass
from pathlib import Path


def sign(a: int) -> int:
    return (a > 0) - (a < 0)


@dataclass
class Vector2:
    x: int
    y: int


def parse_target_area(input_str: str) -> tuple[tuple[int, int], tuple[int, int]]:
    parsed_target_area = [
        list(map(int, bounds[2:].split("..")))
        for bounds in input_str.lstrip("target area: ").split(", ")
    ]

    return (
        (parsed_target_area[0][0], parsed_target_area[0][1]),
        (parsed_target_area[1][0], parsed_target_area[1][1]),
    )


def compute_position(initial_velocity: Vector2, num_steps: int) -> Vector2:
    (vx, vy) = (initial_velocity.x, initial_velocity.y)
    x = int(min(num_steps, abs(vx)) * (vx - sign(vx) * (min(num_steps, abs(vx)) - 1) / 2))
    y = int(num_steps * (vy - (num_steps - 1) / 2))

    return Vector2(x, y)


def part_one(target_area: tuple[tuple[int, int], tuple[int, int]]) -> int:
    ((min_x, max_x), (min_y, max_y)) = target_area
    print(min_x, max_x, min_y, max_y)

    print(Vector2(7, 2), 7, compute_position(Vector2(7, 2), 7))
    print(Vector2(6, 3), 9, compute_position(Vector2(6, 3), 9))
    print(Vector2(9, 0), 4, compute_position(Vector2(9, 0), 4))
    print(Vector2(-2, -4), 4, compute_position(Vector2(-2, -4), 4))

    return 0


def part_two(target_area: tuple[tuple[int, int], tuple[int, int]]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    target_area = parse_target_area(problem_input[0])

    print("Part One: ", part_one(target_area))
    print("Part Two: ", part_two(target_area))
