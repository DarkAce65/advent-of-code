from collections import defaultdict
from enum import Enum, unique
from pathlib import Path


@unique
class CaveSize(str, Enum):
    BIG = "BIG"
    SMALL = "SMALL"


class CaveNode:
    name: str
    size: CaveSize

    connected_cave_names: set[str]

    def __init__(self, name: str) -> None:
        self.name = name
        self.size = CaveSize.BIG if self.name.isupper() else CaveSize.SMALL
        self.connected_cave_names = set()


class CaveGraph:
    caves: dict[str, CaveNode]

    def __init__(self, graph_definition: list[str]) -> None:
        self.caves = {}
        for edge in graph_definition:
            (left_node, right_node) = edge.split("-")
            if left_node not in self.caves:
                self.caves[left_node] = CaveNode(left_node)
            if right_node not in self.caves:
                self.caves[right_node] = CaveNode(right_node)

            self.caves[left_node].connected_cave_names.add(right_node)
            self.caves[right_node].connected_cave_names.add(left_node)

    def get_cave(self, cave_name: str) -> CaveNode:
        return self.caves[cave_name]

    def get_small_caves(self) -> set[str]:
        return set(
            map(
                lambda cave: cave.name,
                filter(lambda cave: cave.size == CaveSize.SMALL, self.caves.values()),
            )
        )


def find_paths(
    cave_graph: CaveGraph,
    current_cave_name: str,
    previously_exhausted_caves: set[str],
) -> int:
    if current_cave_name == "end":
        return 1

    current_cave = cave_graph.get_cave(current_cave_name)

    exhausted_caves = previously_exhausted_caves
    if current_cave.size == CaveSize.SMALL:
        exhausted_caves = exhausted_caves.copy()
        exhausted_caves.add(current_cave_name)

    caves_to_visit = current_cave.connected_cave_names.difference(exhausted_caves)

    if len(caves_to_visit) == 0:
        return 0

    return sum(
        find_paths(cave_graph, cave_to_visit, exhausted_caves)
        for cave_to_visit in caves_to_visit
    )


def part_one(cave_graph: CaveGraph) -> int:
    return find_paths(cave_graph, "start", set())


def find_paths_visiting_small_caves_twice(
    cave_graph: CaveGraph,
    current_cave_name: str,
    previous_small_cave_visits: defaultdict[str, int] = defaultdict(int),
) -> int:
    if current_cave_name == "end":
        return 1

    current_cave = cave_graph.get_cave(current_cave_name)

    small_cave_visits = previous_small_cave_visits
    if current_cave.size == CaveSize.SMALL:
        small_cave_visits = small_cave_visits.copy()
        small_cave_visits[current_cave_name] += 1

    if any(visits >= 2 for visits in small_cave_visits.values()):
        caves_to_visit = current_cave.connected_cave_names.difference(
            set(small_cave_visits.keys())
        )
    else:
        caves_to_visit = current_cave.connected_cave_names.difference(set(["start"]))

    if len(caves_to_visit) == 0:
        return 0

    return sum(
        find_paths_visiting_small_caves_twice(
            cave_graph, cave_to_visit, small_cave_visits
        )
        for cave_to_visit in caves_to_visit
    )


def part_two(cave_graph: CaveGraph) -> int:
    return find_paths_visiting_small_caves_twice(cave_graph, "start")


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    cave_graph = CaveGraph(problem_input)

    print("Part One: ", part_one(cave_graph))
    print("Part Two: ", part_two(cave_graph))
