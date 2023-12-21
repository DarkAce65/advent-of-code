from enum import Enum

from utils import get_and_cache_input


class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


class Comparison(Enum):
    UNKNOWN = 1
    BETTER = 2
    WORSE = 3
    EQUAL = 4


Position = tuple[int, int]
Heading = tuple[Direction, int]


def get_next_positions_and_headings(
    position: Position,
    heading: Heading,
    num_rows: int,
    num_cols: int,
    min_movement=0,
    max_movement=3,
) -> list[tuple[Position, Heading]]:
    next_positions_and_headings = []

    if (
        (heading[0] == Direction.UP and heading[1] < max_movement)
        or (
            (heading[0] == Direction.RIGHT or heading[0] == Direction.LEFT)
            and heading[1] >= min_movement
        )
    ) and position[0] > 0:
        next_position = (position[0] - 1, position[1])
        next_heading = (
            Direction.UP,
            heading[1] + 1 if heading[0] == Direction.UP else 1,
        )
        next_positions_and_headings.append((next_position, next_heading))
    if (
        (heading[0] == Direction.RIGHT and heading[1] < max_movement)
        or (
            (heading[0] == Direction.UP or heading[0] == Direction.DOWN)
            and heading[1] >= min_movement
        )
    ) and position[1] + 1 < num_cols:
        next_position = (position[0], position[1] + 1)
        next_heading = (
            Direction.RIGHT,
            heading[1] + 1 if heading[0] == Direction.RIGHT else 1,
        )
        next_positions_and_headings.append((next_position, next_heading))
    if (
        (heading[0] == Direction.DOWN and heading[1] < max_movement)
        or (
            (heading[0] == Direction.RIGHT or heading[0] == Direction.LEFT)
            and heading[1] >= min_movement
        )
    ) and position[0] + 1 < num_rows:
        next_position = (position[0] + 1, position[1])
        next_heading = (
            Direction.DOWN,
            heading[1] + 1 if heading[0] == Direction.DOWN else 1,
        )
        next_positions_and_headings.append((next_position, next_heading))
    if (
        (heading[0] == Direction.LEFT and heading[1] < max_movement)
        or (
            (heading[0] == Direction.UP or heading[0] == Direction.DOWN)
            and heading[1] >= min_movement
        )
    ) and position[1] > 0:
        next_position = (position[0], position[1] - 1)
        next_heading = (
            Direction.LEFT,
            heading[1] + 1 if heading[0] == Direction.LEFT else 1,
        )
        next_positions_and_headings.append((next_position, next_heading))

    return next_positions_and_headings


def find_best_path(problem_input: list[str], min_movement: int, max_movement: int) -> int:
    num_rows = len(problem_input)
    num_cols = len(problem_input[0])
    end_position = (num_rows - 1, num_cols - 1)

    iterations = 0

    to_visit: list[tuple[Position, Heading]] = []
    best_states: dict[tuple[Position, Heading], int] = {}

    to_visit.append(((0, 0), (Direction.RIGHT, 0)))
    best_states[((0, 0), (Direction.RIGHT, 0))] = 0
    while len(to_visit) > 0:
        position, heading = to_visit.pop(0)
        heat_loss = best_states[(position, heading)]

        if position == end_position or iterations % 100_000 == 0:
            print(
                heat_loss,
                "*" if position == end_position else "",
                "\t",
                position,
                "\t",
                heading[0].value + " " + str(heading[1]),
                "\t",
                len(to_visit),
            )

        for next_position, next_heading in get_next_positions_and_headings(
            position, heading, num_rows, num_cols, min_movement, max_movement
        ):
            next_heat_loss = heat_loss + int(
                problem_input[next_position[0]][next_position[1]]
            )
            next_state = (next_position, next_heading)
            if next_state not in best_states or next_heat_loss < best_states[next_state]:
                best_states[next_state] = next_heat_loss
                to_visit.append(next_state)
        iterations += 1

    best_heat_loss: int | None = None
    for state in best_states:
        if state[0] == end_position and (
            best_heat_loss is None or best_states[state] < best_heat_loss
        ):
            best_heat_loss = best_states[state]
    assert best_heat_loss is not None, "No path found"

    return best_heat_loss


def part_one(problem_input: list[str]) -> int:
    return find_best_path(problem_input, 0, 3)


def part_two(problem_input: list[str]) -> int:
    return find_best_path(problem_input, 4, 10)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
