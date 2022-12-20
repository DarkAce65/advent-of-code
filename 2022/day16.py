import re
from collections import defaultdict, deque
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
    path_to_valve: dict[str, int]

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

            neighbors = [
                node
                for node in self.nodes[node].to_valves.difference(visited_nodes)
                if node not in nodes_to_visit
            ]
            nodes_to_visit.extend((node, n) for n in neighbors)

        raise ValueError("Couldn't find end")

    def compute_distances(self):
        for start_node in self.nodes.keys():
            for end_node in self.nodes.keys():
                if start_node + "-" + end_node in self.path_to_valve:
                    continue

                path_len = len(self.bfs(start_node, end_node))
                self.path_to_valve[start_node + "-" + end_node] = path_len
                self.path_to_valve[end_node + "-" + start_node] = path_len

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

            time_to_open_valve = self.path_to_valve[current_node + "-" + node] + 1
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


class DoubleWalkValveSolver:
    valve_flows: dict[str, int]
    time_to_open_valve: defaultdict[str, dict[str, int]]

    def __init__(self, graph: ValveGraph) -> None:
        self.valve_flows = {}
        self.time_to_open_valve = defaultdict(dict)

        for node in graph.nodes.values():
            if node.name == "AA" or node.flow_rate > 0:
                self.valve_flows[node.name] = node.flow_rate

        for key, path_len in graph.path_to_valve.items():
            from_node, to_node = key.split("-")
            if (
                from_node == "AA"
                or to_node == "AA"
                or (from_node in self.valve_flows and to_node in self.valve_flows)
            ):
                self.time_to_open_valve[from_node][to_node] = path_len + 1

    def find_optimal_pressure_with_elephant(self, total_time: int) -> int:
        valves_to_open = set(
            valve for valve, flow_rate in self.valve_flows.items() if flow_rate > 0
        )

        possible_states: deque[
            tuple[tuple[str, int], tuple[str, int], frozenset[str], int, int]
        ] = deque()
        cache: dict[tuple[frozenset[tuple[str, int]], frozenset[str], int], int] = {}
        cache_stats = [0, 0]

        possible_states.append((("AA", 0), ("AA", 0), frozenset(), total_time, 0))

        optimal_pressure = 0
        while len(possible_states) > 0:
            (
                walker_1,
                walker_2,
                open_valves,
                time_left,
                current_pressure,
            ) = possible_states.popleft()

            open_valve_pressure = sum(self.valve_flows[valve] for valve in open_valves)
            cache_key = (frozenset([walker_1, walker_2]), open_valves, time_left)
            if cache_key in cache and current_pressure <= cache[cache_key]:
                cache_stats[0] += 1
                continue
            cache_stats[1] += 1
            cache[cache_key] = current_pressure

            closed_valves = valves_to_open.difference(open_valves)
            if len(closed_valves) == 0 or time_left == 0:
                pressure = current_pressure + time_left * open_valve_pressure
                if optimal_pressure < pressure:
                    optimal_pressure = pressure
                    print(optimal_pressure, cache_stats)
                continue

            for closed_valve in closed_valves:
                # Advance walker_1
                time_cost = (
                    self.time_to_open_valve[walker_1[0]][closed_valve] - walker_1[1]
                )
                if 0 <= time_cost and time_cost <= time_left:
                    possible_states.appendleft(
                        (
                            (closed_valve, 0),
                            (walker_2[0], walker_2[1] + time_cost),
                            open_valves.union([closed_valve]),
                            time_left - time_cost,
                            current_pressure + time_cost * open_valve_pressure,
                        )
                    )
                # Advance walker_2
                time_cost = (
                    self.time_to_open_valve[walker_2[0]][closed_valve] - walker_2[1]
                )
                if 0 <= time_cost and time_cost <= time_left:
                    possible_states.appendleft(
                        (
                            (walker_1[0], walker_1[1] + time_cost),
                            (closed_valve, 0),
                            open_valves.union([closed_valve]),
                            time_left - time_cost,
                            current_pressure + time_cost * open_valve_pressure,
                        )
                    )

        print(optimal_pressure, cache_stats)

        return optimal_pressure


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


def part_two(problem_input: list[str]) -> int:
    graph = ValveGraph()

    for line in problem_input:
        node = parse_valve_node(line)
        graph.add_node(node)

    graph.compute_distances()
    solver = DoubleWalkValveSolver(graph)

    return solver.find_optimal_pressure_with_elephant(26)


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
