import math
from pathlib import Path
from typing import Optional


def sign(a: int) -> int:
    return (a > 0) - (a < 0)


def is_perfect_square(a: int) -> bool:
    root = int(math.sqrt(a))
    return root ** 2 == a


def parse_target_area(input_str: str) -> tuple[tuple[int, int], tuple[int, int]]:
    parsed_target_area = [
        list(map(int, bounds[2:].split("..")))
        for bounds in input_str.lstrip("target area: ").split(", ")
    ]

    return (
        (parsed_target_area[0][0], parsed_target_area[0][1]),
        (parsed_target_area[1][0], parsed_target_area[1][1]),
    )


def compute_position(vx: int, vy: int, num_steps: int) -> tuple[int, int]:
    x = int(min(num_steps, abs(vx)) * (vx - sign(vx) * (min(num_steps, abs(vx)) - 1) / 2))
    y = int(num_steps * (vy - (num_steps - 1) / 2))

    return (x, y)


def get_y_candidates(min_y: int, max_y: int) -> list[tuple[int, int]]:
    if min_y < 0 and 0 < max_y:
        raise ValueError("Infinite candidates for the given range")

    candidates = []

    current_steps = 2 * max(abs(min_y), abs(max_y))
    while current_steps > 0:
        for candidate in range(
            math.ceil(min_y / current_steps + (current_steps - 1) / 2),
            math.floor(max_y / current_steps + (current_steps - 1) / 2) + 1,
        ):
            candidates.append((candidate, current_steps))
        current_steps -= 1

    return candidates


def get_tail_x_candidate(min_x: int, max_x: int, target_steps: int) -> Optional[int]:
    triangles = set()
    for x in range(min_x, max_x + 1):
        if is_perfect_square(8 * abs(x) + 1):
            triangles.add(x)

    x_candidates = sorted(
        filter(
            lambda n: n <= target_steps,
            map(lambda t: sign(t) * int((math.sqrt(8 * abs(t) + 1) - 1) / 2), triangles),
        ),
        key=abs,
    )

    if len(x_candidates) == 0:
        return None

    return x_candidates[0]


def part_one(target_area: tuple[tuple[int, int], tuple[int, int]]) -> int:
    ((min_x, max_x), (min_y, max_y)) = target_area

    velocity = None
    target_steps = None

    y_candidates = get_y_candidates(min_y, max_y)
    for (y_candidate, steps) in y_candidates:
        x_candidate = get_tail_x_candidate(min_x, max_x, steps)
        if x_candidate is not None:
            velocity = (x_candidate, y_candidate)
            target_steps = steps
            break

    if velocity is None or target_steps is None:
        raise ValueError("No trajectory found")

    (_, vy) = velocity
    return int(min(target_steps, abs(vy)) * (vy - (min(target_steps, abs(vy)) - 1) / 2))


def get_x_values(min_x: int, max_x: int, y: int, steps: int) -> list[int]:
    x_candidates = []

    for x in range(max_x + 1):
        (pos_x, _) = compute_position(x, y, steps)
        if min_x <= pos_x and pos_x <= max_x:
            x_candidates.append(x)

    return x_candidates


def part_two(target_area: tuple[tuple[int, int], tuple[int, int]]) -> int:
    ((min_x, max_x), (min_y, max_y)) = target_area

    velocities = set()

    y_candidates = get_y_candidates(min_y, max_y)
    for (y_candidate, steps) in y_candidates:
        x_candidates = get_x_values(min_x, max_x, y_candidate, steps)
        for x in x_candidates:
            velocities.add((x, y_candidate))

    return len(velocities)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    target_area = parse_target_area(problem_input[0])

    print("Part One: ", part_one(target_area))
    print("Part Two: ", part_two(target_area))
