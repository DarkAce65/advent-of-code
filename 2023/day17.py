from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from typing import Literal
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


@dataclass(frozen=True)
class State:
    heat_loss: int
    heading: Heading

    def compare(self, other: State, min_movement=0) -> Comparison:
        if self.heat_loss == other.heat_loss and self.heading == other.heading:
            return Comparison.EQUAL
        elif (
            self.heat_loss <= other.heat_loss
            and self.heading[0] == other.heading[0]
            and min_movement <= self.heading[1] <= other.heading[1]
        ):
            return Comparison.BETTER
        elif (
            self.heat_loss >= other.heat_loss
            and self.heading[0] == other.heading[0]
            and self.heading[1] >= other.heading[1] >= min_movement
        ):
            return Comparison.WORSE

        return Comparison.UNKNOWN

    def get_next_positions_and_headings(
        self,
        position: Position,
        num_rows: int,
        num_cols: int,
        min_movement=0,
        max_movement=3,
    ) -> list[tuple[Position, Heading]]:
        next_positions_and_headings = []

        if (
            (self.heading[0] == Direction.UP and self.heading[1] < max_movement)
            or (
                (self.heading[0] == Direction.RIGHT or self.heading[0] == Direction.LEFT)
                and self.heading[1] >= min_movement
            )
        ) and position[0] > 0:
            next_position = (position[0] - 1, position[1])
            next_heading = (
                Direction.UP,
                self.heading[1] + 1 if self.heading[0] == Direction.UP else 1,
            )
            next_positions_and_headings.append((next_position, next_heading))
        if (
            (self.heading[0] == Direction.RIGHT and self.heading[1] < max_movement)
            or (
                (self.heading[0] == Direction.UP or self.heading[0] == Direction.DOWN)
                and self.heading[1] >= min_movement
            )
        ) and position[1] + 1 < num_cols:
            next_position = (position[0], position[1] + 1)
            next_heading = (
                Direction.RIGHT,
                self.heading[1] + 1 if self.heading[0] == Direction.RIGHT else 1,
            )
            next_positions_and_headings.append((next_position, next_heading))
        if (
            (self.heading[0] == Direction.DOWN and self.heading[1] < max_movement)
            or (
                (self.heading[0] == Direction.RIGHT or self.heading[0] == Direction.LEFT)
                and self.heading[1] >= min_movement
            )
        ) and position[0] + 1 < num_rows:
            next_position = (position[0] + 1, position[1])
            next_heading = (
                Direction.DOWN,
                self.heading[1] + 1 if self.heading[0] == Direction.DOWN else 1,
            )
            next_positions_and_headings.append((next_position, next_heading))
        if (
            (self.heading[0] == Direction.LEFT and self.heading[1] < max_movement)
            or (
                (self.heading[0] == Direction.UP or self.heading[0] == Direction.DOWN)
                and self.heading[1] >= min_movement
            )
        ) and position[1] > 0:
            next_position = (position[0], position[1] - 1)
            next_heading = (
                Direction.LEFT,
                self.heading[1] + 1 if self.heading[0] == Direction.LEFT else 1,
            )
            next_positions_and_headings.append((next_position, next_heading))

        return next_positions_and_headings


def part_one(problem_input: list[str]) -> int:
    num_rows = len(problem_input)
    num_cols = len(problem_input[0])
    end_position = (num_rows - 1, num_cols - 1)

    to_visit: set[Position] = set([(0, 0)])
    best_states: dict[Position, list[State]] = defaultdict(list)
    best_states[(0, 0)].append(State(0, (Direction.RIGHT, 0)))
    while len(to_visit) > 0:
        position = to_visit.pop()
        states = best_states[position]

        for state in states:
            for next_position, next_heading in state.get_next_positions_and_headings(
                position, num_rows, num_cols
            ):
                next_heat_loss = state.heat_loss + int(
                    problem_input[next_position[0]][next_position[1]]
                )
                next_state = State(next_heat_loss, next_heading)

                new_states: list[State] = []
                state_status: Literal["skip", "unknown", "better"] = "unknown"
                for s in best_states[next_position]:
                    compare_result = next_state.compare(s)
                    if (
                        compare_result == Comparison.EQUAL
                        or compare_result == Comparison.WORSE
                    ):
                        state_status = "skip"
                        break
                    elif compare_result == Comparison.BETTER:
                        state_status = "better"
                    elif compare_result == Comparison.UNKNOWN:
                        new_states.append(s)

                if state_status == "skip":
                    continue
                else:
                    new_states.append(next_state)

                best_states[next_position] = new_states
                to_visit.add(next_position)

    if end_position not in best_states:
        raise ValueError("No path found")

    return min(state.heat_loss for state in best_states[end_position])


def part_two(problem_input: list[str]) -> int:
    num_rows = len(problem_input)
    num_cols = len(problem_input[0])
    end_position = (num_rows - 1, num_cols - 1)

    to_visit: set[Position] = set([(0, 0)])
    visited_states: set[tuple[Position, State]] = set()
    best_states: dict[Position, list[State]] = defaultdict(list)
    best_states[(0, 0)].append(State(0, (Direction.RIGHT, 0)))
    best_states[(0, 0)].append(State(0, (Direction.DOWN, 0)))
    while len(to_visit) > 0:
        position = to_visit.pop()
        states = best_states[position]

        for state in states:
            if (position, state) in visited_states:
                continue
            visited_states.add((position, state))
            for next_position, next_heading in state.get_next_positions_and_headings(
                position, num_rows, num_cols, min_movement=4, max_movement=10
            ):
                next_heat_loss = state.heat_loss + int(
                    problem_input[next_position[0]][next_position[1]]
                )
                next_state = State(next_heat_loss, next_heading)

                new_states: list[State] = []
                state_status: Literal["skip", "unknown", "better"] = "unknown"
                for s in best_states[next_position]:
                    compare_result = next_state.compare(s, min_movement=4)
                    if (
                        compare_result == Comparison.EQUAL
                        or compare_result == Comparison.WORSE
                    ):
                        state_status = "skip"
                        break
                    elif compare_result == Comparison.BETTER:
                        state_status = "better"
                    elif compare_result == Comparison.UNKNOWN:
                        new_states.append(s)

                if state_status == "skip":
                    continue
                else:
                    new_states.append(next_state)

                best_states[next_position] = new_states
                to_visit.add(next_position)

    if end_position not in best_states:
        raise ValueError("No path found")

    return min(
        state.heat_loss for state in best_states[end_position] if state.heading[1] >= 4
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
