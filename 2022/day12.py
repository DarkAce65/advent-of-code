from collections import deque
from pathlib import Path
from typing import Optional

HEIGHTMAP = list("abcdefghijklmnopqrstuvwxyz")


class Map:
    map: list[list[int]]
    start: tuple[int, int]
    end: tuple[int, int]

    def __init__(self, problem_input: list[str]) -> None:
        self.map = []
        for row, line in enumerate(problem_input):
            self.map.append([])
            for col, cell in enumerate(line):
                if cell == "S":
                    self.start = (row, col)
                    self.map[row].append(HEIGHTMAP.index("a"))
                elif cell == "E":
                    self.end = (row, col)
                    self.map[row].append(HEIGHTMAP.index("z"))
                else:
                    self.map[row].append(HEIGHTMAP.index(cell))

    def find_shortest_path(self) -> list[tuple[int, int]]:
        node_to_from_node: dict[tuple[int, int], Optional[tuple[int, int]]] = {}
        nodes_to_visit: deque[tuple[int, int]] = deque()

        nodes_to_visit.append(self.start)
        node_to_from_node[self.start] = None

        found_path = False
        while len(nodes_to_visit) > 0:
            node = nodes_to_visit.popleft()

            if node == self.end:
                found_path = True
                break

            row, col = node
            current_height = self.map[row][col]
            if (
                (row - 1, col) not in node_to_from_node
                and row > 0
                and current_height - self.map[row - 1][col] >= -1
            ):
                nodes_to_visit.append((row - 1, col))
                node_to_from_node[(row - 1, col)] = node
            if (
                (row + 1, col) not in node_to_from_node
                and row < len(self.map) - 1
                and current_height - self.map[row + 1][col] >= -1
            ):
                nodes_to_visit.append((row + 1, col))
                node_to_from_node[(row + 1, col)] = node
            if (
                (row, col - 1) not in node_to_from_node
                and col > 0
                and current_height - self.map[row][col - 1] >= -1
            ):
                nodes_to_visit.append((row, col - 1))
                node_to_from_node[(row, col - 1)] = node
            if (row, col + 1) not in node_to_from_node and (
                col < len(self.map[row]) - 1
                and current_height - self.map[row][col + 1] >= -1
            ):
                nodes_to_visit.append((row, col + 1))
                node_to_from_node[(row, col + 1)] = node

        if not found_path:
            raise ValueError("Couldn't find a path")

        path: list[tuple[int, int]] = []
        path_node: Optional[tuple[int, int]] = self.end
        while path_node is not None:
            path.insert(0, path_node)
            path_node = node_to_from_node[path_node]

        return path


def part_one(problem_input: list[str]) -> int:
    map = Map(problem_input)
    return len(map.find_shortest_path()) - 1


def part_two(problem_input: list[str]) -> int:
    map = Map(problem_input)
    best_distance = len(map.find_shortest_path()) - 1

    possible_starts: set[tuple[int, int]] = set()
    for row in range(len(map.map)):
        for col in range(len(map.map)):
            if map.start != (row, col) and map.map[row][col] == 0:
                possible_starts.add((row, col))

    for start in possible_starts:
        map.start = start
        try:
            distance = len(map.find_shortest_path()) - 1
        except ValueError:
            continue

        if best_distance > distance:
            best_distance = distance

    return best_distance


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
