from typing import Optional

from utils import get_and_cache_input

Position = tuple[int, int]


def get_neighbors(problem_input: list[str], position: Position) -> list[Position]:
    neighbors: list[Position] = []

    next_position = (position[0] - 1, position[1])
    if position[0] > 0 and problem_input[next_position[0]][next_position[1]] != "#":
        neighbors.append(next_position)

    next_position = (position[0], position[1] - 1)
    if position[1] > 0 and problem_input[next_position[0]][next_position[1]] != "#":
        neighbors.append(next_position)

    next_position = (position[0], position[1] + 1)
    if (
        position[1] < len(problem_input[0]) - 1
        and problem_input[next_position[0]][next_position[1]] != "#"
    ):
        neighbors.append(next_position)

    next_position = (position[0] + 1, position[1])
    if (
        position[0] < len(problem_input) - 1
        and problem_input[next_position[0]][next_position[1]] != "#"
    ):
        neighbors.append(next_position)

    return neighbors


def get_neighbors_wrapped(problem_input: list[str], position: Position) -> list[Position]:
    neighbors: list[Position] = []

    next_position = (position[0] - 1, position[1])
    if (
        problem_input[next_position[0] % len(problem_input)][
            next_position[1] % len(problem_input[0])
        ]
        != "#"
    ):
        neighbors.append(next_position)

    next_position = (position[0], position[1] - 1)
    if (
        problem_input[next_position[0] % len(problem_input)][
            next_position[1] % len(problem_input[0])
        ]
        != "#"
    ):
        neighbors.append(next_position)

    next_position = (position[0], position[1] + 1)
    if (
        problem_input[next_position[0] % len(problem_input)][
            next_position[1] % len(problem_input[0])
        ]
        != "#"
    ):
        neighbors.append(next_position)

    next_position = (position[0] + 1, position[1])
    if (
        problem_input[next_position[0] % len(problem_input)][
            next_position[1] % len(problem_input[0])
        ]
        != "#"
    ):
        neighbors.append(next_position)

    return neighbors


def get_reachable_positions(
    problem_input: list[str],
    starting_position: Position,
    max_steps: Optional[int] = None,
    wrap_edges=False,
) -> dict[Position, int]:
    to_visit: list[Position] = []
    best_steps: dict[Position, int] = {}

    to_visit.append(starting_position)
    best_steps[starting_position] = 0
    while len(to_visit) > 0:
        position = to_visit.pop(0)
        steps = best_steps[position]
        best_steps[position] = steps

        if max_steps is None or steps < max_steps:
            for neighbor in (
                get_neighbors(problem_input, position)
                if not wrap_edges
                else get_neighbors_wrapped(problem_input, position)
            ):
                if neighbor not in best_steps or steps + 1 < best_steps[neighbor]:
                    best_steps[neighbor] = steps + 1
                    to_visit.append(neighbor)

    return best_steps


def part_one(problem_input: list[str]) -> int:
    starting_position: Position | None = None
    for row, line in enumerate(problem_input):
        if "S" in line:
            starting_position = (row, line.index("S"))
            break
    assert starting_position is not None

    best_steps = get_reachable_positions(problem_input, starting_position, max_steps=64)

    return sum(1 for steps in best_steps.values() if steps % 2 == 0)


def part_two(problem_input: list[str]) -> int:
    x = int((26501365 - int(len(problem_input) / 2)) / len(problem_input))
    print(x)

    starting_position: Position | None = None
    for row, line in enumerate(problem_input):
        if "S" in line:
            starting_position = (row, line.index("S"))
            break
    assert starting_position is not None

    best_steps = get_reachable_positions(
        problem_input,
        starting_position,
        max_steps=int(len(problem_input) * 2.5),
        wrap_edges=True,
    )
    locations = set(position for position, steps in best_steps.items() if steps % 2 == 1)
    locations_by_grid: dict[Position, int] = {}
    for r in range(-2, 3):
        for c in range(-2, 3):
            locations_by_grid[(r, c)] = sum(
                1
                for location in locations
                if r * len(problem_input) <= location[0] < (r + 1) * len(problem_input)
                and c * len(problem_input[0])
                <= location[1]
                < (c + 1) * len(problem_input[0])
            )

    scale_factor = int(
        (26501365 - int(len(problem_input) / 2)) / len(problem_input)
    )  # 202300

    outer_corners = int(
        locations_by_grid[(-2, 0)]
        + locations_by_grid[(0, -2)]
        + locations_by_grid[(0, 2)]
        + locations_by_grid[(2, 0)]
    )
    outer_edges = int(
        (
            locations_by_grid[(-2, -1)]
            + locations_by_grid[(-2, 1)]
            + locations_by_grid[(-1, -2)]
            + locations_by_grid[(-1, 2)]
            + locations_by_grid[(1, -2)]
            + locations_by_grid[(1, 2)]
            + locations_by_grid[(2, -1)]
            + locations_by_grid[(2, 1)]
        )
        * scale_factor
        / 2  # Every scaled grid expands edges by half
    )
    inner_corners = int(
        (
            locations_by_grid[(-1, -1)]
            + locations_by_grid[(-1, 1)]
            + locations_by_grid[(1, -1)]
            + locations_by_grid[(1, 1)]
        )
        * (scale_factor - 1)
    )
    inner_edges = int(
        (
            locations_by_grid[(-1, 0)]
            + locations_by_grid[(0, -1)]
            + locations_by_grid[(0, 1)]
            + locations_by_grid[(1, 0)]
        )
        * scale_factor
        * scale_factor
        / 4
    )
    middle = int(locations_by_grid[(0, 0)] * (scale_factor - 1) * (scale_factor - 1))
    return outer_corners + outer_edges + inner_corners + inner_edges + middle


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
