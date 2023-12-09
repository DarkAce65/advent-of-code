import math
from collections import deque

from utils import get_and_cache_input

Position = tuple[int, int]


def insert_into_sorted_deque(
    values: deque[tuple[Position, int]], item_to_insert: tuple[Position, int]
):
    for i, item in enumerate(values):
        if item[1] > item_to_insert[1]:
            values.insert(i, item_to_insert)
            return

    values.append(item_to_insert)


class BlizzardMap:
    start: Position
    end: Position
    width: int
    height: int
    blizzards: set[tuple[Position, str]]

    wall_cache: dict[int, set[Position]]
    time_multiple: int

    def __init__(self, map_input: list[str]) -> None:
        self.width = len(map_input[0]) - 2
        self.height = len(map_input) - 2
        self.blizzards = set()
        for row, line in enumerate(map_input):
            for col, c in enumerate(line):
                if c == ".":
                    if row == 0:
                        self.start = (row, col)
                    elif row == len(map_input) - 1:
                        self.end = (row, col)
                    continue
                elif c == "#":
                    continue

                self.blizzards.add(((row, col), c))

        self.wall_cache = {}
        self.time_multiple = math.lcm(self.width, self.height)

    def get_walls(self, time: int) -> set[Position]:
        time = time % self.time_multiple
        if time in self.wall_cache:
            return self.wall_cache[time]

        walls = set()

        for blizzard, direction in self.blizzards:
            if direction == ">":
                walls.add((blizzard[0], (blizzard[1] + time - 1) % self.width + 1))
            elif direction == "v":
                walls.add(((blizzard[0] + time - 1) % self.height + 1, blizzard[1]))
            elif direction == "<":
                walls.add((blizzard[0], (blizzard[1] - time - 1) % self.width + 1))
            elif direction == "^":
                walls.add(((blizzard[0] - time - 1) % self.height + 1, blizzard[1]))
            else:
                raise ValueError("Unrecognized direction `" + direction + "`")

        self.wall_cache[time] = walls
        return walls

    def print_map(self, time: int):
        walls: dict[Position, str] = {}

        for blizzard, direction in self.blizzards:
            if direction == ">":
                walls[
                    (blizzard[0], (blizzard[1] + time - 1) % self.width + 1)
                ] = direction
            elif direction == "v":
                walls[
                    ((blizzard[0] + time - 1) % self.height + 1, blizzard[1])
                ] = direction
            elif direction == "<":
                walls[
                    (blizzard[0], (blizzard[1] - time - 1) % self.width + 1)
                ] = direction
            elif direction == "^":
                walls[
                    ((blizzard[0] - time - 1) % self.height + 1, blizzard[1])
                ] = direction

        for row in range(self.height + 2):
            row_str = ""
            for col in range(self.width + 2):
                if (row, col) in walls:
                    row_str += walls[(row, col)]
                elif (
                    (
                        row == 0
                        or row == self.height + 1
                        or col == 0
                        or col == self.width + 1
                    )
                    and (row, col) != self.start
                    and (row, col) != self.end
                ):
                    row_str += "#"
                else:
                    row_str += "."
            print(row_str)

    def is_node_walkable(self, position: Position, time: int) -> bool:
        return (
            position == self.start
            or position == self.end
            or (
                0 < position[0] < self.height + 1
                and 0 < position[1] < self.width + 1
                and position not in self.get_walls(time)
            )
        )

    def find_shortest_path(self, start: Position, end: Position, start_time=0) -> int:
        nodes_to_visit: deque[tuple[Position, int]] = deque()
        states_considered: set[tuple[Position, int]] = set()

        nodes_to_visit.append((start, start_time))

        while len(nodes_to_visit) > 0:
            position, time = nodes_to_visit.popleft()
            if position == end:
                return time

            next_time = time + 1
            neighbors: list[Position] = [
                (position[0], position[1] + 1),
                (position[0] + 1, position[1]),
                (position[0], position[1] - 1),
                (position[0] - 1, position[1]),
                (position[0], position[1]),
            ]
            for neighbor in neighbors:
                if (
                    self.is_node_walkable(neighbor, next_time)
                    and (neighbor, next_time % self.time_multiple)
                    not in states_considered
                ):
                    insert_into_sorted_deque(nodes_to_visit, (neighbor, next_time))
                    states_considered.add((neighbor, next_time % self.time_multiple))

        raise ValueError("Could not find path")


def part_one(problem_input: list[str]) -> int:
    blizzard_map = BlizzardMap(problem_input)
    return blizzard_map.find_shortest_path(blizzard_map.start, blizzard_map.end)


def part_two(problem_input: list[str]) -> int:
    blizzard_map = BlizzardMap(problem_input)
    to_end = blizzard_map.find_shortest_path(blizzard_map.start, blizzard_map.end)
    back_to_start = blizzard_map.find_shortest_path(
        blizzard_map.end, blizzard_map.start, to_end
    )
    back_to_end = blizzard_map.find_shortest_path(
        blizzard_map.start, blizzard_map.end, back_to_start
    )
    return back_to_end


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
