import re
from collections import deque
from pathlib import Path
from typing import cast


class ValveNode:
    name: str
    flow_rate: int
    to_valves: set[str]

    def __init__(self, name: str, flow_rate: int, to_valves: set[str]) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.to_valves = to_valves


class ValveGraph:
    nodes: dict[str, ValveNode]
    path_to_valve: dict[str, list[str]]

    def __init__(self) -> None:
        self.nodes = {}
        self.path_to_valve = {}

    def add_node(self, node: ValveNode):
        self.nodes[node.name] = node

    def bfs(self, start: str, end: str) -> list[str]:
        nodes_to_visit: deque[tuple[str | None, str]] = deque()
        visited_nodes: dict[str, str | None] = {}
        nodes_to_visit.append((None, start))

        while len(nodes_to_visit) > 0:
            prev_node, node = nodes_to_visit.popleft()
            visited_nodes[node] = prev_node

            if node == end:
                path: list[str] = []
                while node != start:
                    path.insert(0, cast(str, visited_nodes[node]))
                    node = cast(str, visited_nodes[node])
                return path

            nodes_to_visit.extend(
                (node, n) for n in self.nodes[node].to_valves.difference(visited_nodes)
            )

        raise ValueError("Couldn't find end")

    def compute_distances(self):
        for start_node in self.nodes.keys():
            for end_node in self.nodes.keys():
                if start_node + "-" + end_node in self.path_to_valve:
                    continue

                path = self.bfs(start_node, end_node)
                self.path_to_valve[start_node + "-" + end_node] = path
                self.path_to_valve[end_node + "-" + start_node] = path

    def find_optimal_pressure(
        self,
        current_node: str = "AA",
        open_valves: list[str] = list(),
        time_left: int = 30,
    ) -> int:
        if time_left == 0:
            return 0

        current_pressure = sum(
            self.nodes[open_valve].flow_rate for open_valve in open_valves
        )
        if len(open_valves) == sum(
            1 for node in self.nodes.values() if node.flow_rate > 0
        ):
            return current_pressure * time_left

        best_pressure = current_pressure * time_left
        for node in self.nodes:
            if self.nodes[node].flow_rate == 0 or node in open_valves:
                continue

            time_to_open_valve = len(self.path_to_valve[current_node + "-" + node]) + 1
            if time_left - time_to_open_valve < 0:
                continue

            new_open_valves = open_valves.copy()
            new_open_valves.append(node)
            pressure = current_pressure * time_to_open_valve + self.find_optimal_pressure(
                node, new_open_valves, time_left - time_to_open_valve
            )
            if pressure > best_pressure:
                best_pressure = pressure

        return best_pressure

    def find_optimal_pressure_with_elephant(
        self,
        steps: list[str],
        elephant_steps: list[str],
        open_valves: set[str] = set(),
        time_left=26,
    ) -> int:
        if time_left == 0:
            return 0

        current_pressure = sum(
            self.nodes[open_valve].flow_rate for open_valve in open_valves
        )

        if len(steps) == 0 and len(elephant_steps) == 0:
            return current_pressure * time_left
        elif len(steps) == 0:
            return current_pressure + self.find_optimal_pressure_with_elephant(
                [], elephant_steps[1:], open_valves, time_left - 1
            )
        elif len(elephant_steps) == 0:
            return current_pressure + self.find_optimal_pressure_with_elephant(
                steps[1:], [], open_valves, time_left - 1
            )

        node_candidates: list[list[str]] = []
        elephant_node_candidates: list[list[str]] = []
        if len(steps) > 1 and len(elephant_steps) > 1:
            return current_pressure + self.find_optimal_pressure_with_elephant(
                steps[1:], elephant_steps[1:], open_valves, time_left - 1
            )
        elif len(steps) == 1 and len(elephant_steps) > 1:
            for node in self.nodes:
                if (
                    self.nodes[node].flow_rate == 0
                    or node in open_valves
                    or node == elephant_steps[-1]
                ):
                    continue

                path = self.path_to_valve[steps[0] + "-" + node]
                time_to_open_valve = len(path) + 1
                if time_left - time_to_open_valve >= 0:
                    node_candidates.append(path)

            if len(node_candidates) == 0:
                return current_pressure + (
                    self.find_optimal_pressure_with_elephant(
                        [], elephant_steps[1:], open_valves, time_left - 1
                    )
                )

            new_open_valves = open_valves.copy()
            new_open_valves.add(elephant_steps[0])
            return current_pressure + max(
                self.find_optimal_pressure_with_elephant(
                    new_steps, elephant_steps[1:], new_open_valves, time_left - 1
                )
                for new_steps in node_candidates
            )
        elif len(steps) > 1 and len(elephant_steps) == 1:
            for node in self.nodes:
                if (
                    self.nodes[node].flow_rate == 0
                    or node in open_valves
                    or node == steps[-1]
                ):
                    continue

                path = self.path_to_valve[steps[0] + "-" + node]
                time_to_open_valve = len(path) + 1
                if time_left - time_to_open_valve >= 0:
                    elephant_node_candidates.append(path)

            if len(elephant_node_candidates) == 0:
                return current_pressure + (
                    self.find_optimal_pressure_with_elephant(
                        steps[1:], [], open_valves, time_left - 1
                    )
                )

            new_open_valves = open_valves.copy()
            new_open_valves.add(elephant_steps[0])
            return current_pressure + max(
                self.find_optimal_pressure_with_elephant(
                    steps[1:], new_elephant_steps, new_open_valves, time_left - 1
                )
                for new_elephant_steps in elephant_node_candidates
            )
        elif len(steps) == 1 and len(elephant_steps) == 1:
            for node in self.nodes:
                if self.nodes[node].flow_rate == 0 or node in open_valves:
                    continue

                path = self.path_to_valve[steps[0] + "-" + node]
                time_to_open_valve = len(path) + 1
                if time_left - time_to_open_valve >= 0:
                    node_candidates.append(path)

                path = self.path_to_valve[elephant_steps[0] + "-" + node]
                time_to_open_valve = len(path) + 1
                if time_left - time_to_open_valve >= 0:
                    elephant_node_candidates.append(path)

            new_open_valves = open_valves.copy()
            new_open_valves.add(steps[0])
            new_open_valves.add(elephant_steps[0])

            candidates: list[tuple[list[str], list[str]]] = []
            node_candidates.append([])
            elephant_node_candidates.append([])
            for path in node_candidates:
                for elephant_path in elephant_node_candidates:
                    if (
                        len(path) > 0
                        and len(elephant_path) > 0
                        and path[-1] == elephant_path[-1]
                    ):
                        continue

                    candidates.append((path, elephant_path))

            if len(candidates) == 0:
                return current_pressure * time_left

            return current_pressure + max(
                self.find_optimal_pressure_with_elephant(
                    new_steps, new_elephant_steps, new_open_valves, time_left - 1
                )
                for new_steps, new_elephant_steps in candidates
            )

        raise NotImplementedError


# class DoubleWalkValveSolver:
#     optimal_single_walk: int
#     valve_flows: dict[str, int]
#     time_to_open_valve: dict[str, dict[str, int]]

#     def __init__(self, graph: ValveGraph) -> None:
#         self.optimal_single_walk = graph.find_optimal_pressure(time_left=26)
#         self.valve_flows = {}
#         self.time_to_open_valve = {}

#         for node in graph.nodes.values():
#             if node.name == "AA" or node.flow_rate > 0:
#                 self.valve_flows[node.name] = node.flow_rate
#                 for to_node in node.to_valves:
#                     if graph.nodes[to_node].flow_rate > 0:
#                         self.time_to_open_valve[(node.name, to_node)] = (
#                             len(graph.path_to_valve) + 1
#                         )
#         for key, path in graph.path_to_valve.items():
#             from_node, to_node = key.split("-")
#             if (
#                 from_node == "AA"
#                 or to_node == "AA"
#                 or (from_node in self.nodes and to_node in self.nodes)
#             ):
#                 self.time_to_open_valve[(from_node, to_node)] = len(path) + 1

#     def complete_sequence(
#         self, sequence_start: list[tuple[int, list[str]]]
#     ) -> list[list[tuple[int, list[str]]]]:
#         sequences: list[list[tuple[int, list[str]]]] = []
#         open_valves: set[str] = set()
#         time_left = 26
#         while time_left >= 0:
#             you = "AA"
#             elephant = "AA"
#             time_left -= 1

#         if len(sequences) == 0:
#             sequences.append(sequence_start)
#         return sequences

#     def compute_sequence_pressure(self, sequence: list[tuple[int, list[str]]]) -> int:
#         pressure = 0
#         for time, opened_valves in sequence:
#             for valve in opened_valves:
#                 pressure += (26 - time) * self.nodes[valve].flow_rate

#         return pressure

#     def compute_possible_paths(
#         self, from_node: str, ignore_valves: set[str], time_left: int
#     ) -> list[tuple[str, int]]:
#         possible_paths: list[tuple[str, int]] = []
#         for to_node in self.time_to_open_valve[from_node]:
#             if (
#                 to_node not in ignore_valves
#                 and self.time_to_open_valve[from_node][to_node] < time_left
#             ):
#                 possible_paths.append(
#                     (to_node, self.time_to_open_valve[from_node][to_node])
#                 )

#         return possible_paths

#     def find_optimal_pressure_with_elephant(
#         self,
#     ) -> int:
#         sequences: list[list[tuple[int, list[str]]]] = self.complete_sequence([])

#         open_valves: set[str] = set()

#         return max(self.compute_sequence_pressure(sequence) for sequence in sequences)


def parse_valve_node(line: str) -> ValveNode:
    match = re.match(
        r"Valve ([A-Z]{2}) has flow rate=(\-?\d+); tunnels? leads? to valves? ([A-Z,\s]+)",
        line,
    )
    if match is None:
        raise ValueError(line)

    valve_name, flow_rate, to_valves = match.groups()

    return ValveNode(
        valve_name, int(flow_rate), set(to.strip() for to in to_valves.strip().split(","))
    )


def part_one(problem_input: list[str]) -> int:
    graph = ValveGraph()

    for line in problem_input:
        node = parse_valve_node(line)
        graph.add_node(node)

    graph.compute_distances()

    return graph.find_optimal_pressure()


# def part_two(problem_input: list[str]) -> int:
#     graph = ValveGraph()

#     for line in problem_input:
#         node = parse_valve_node(line)
#         graph.add_node(node)

#     graph.compute_distances()
#     solver = DoubleWalkValveSolver(graph)

#     return solver.find_optimal_pressure_with_elephant()


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    # print("Part Two: ", part_two(problem_input))
