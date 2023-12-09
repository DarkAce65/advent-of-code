import math
import re
from dataclasses import dataclass

from utils import get_and_cache_input


@dataclass
class Node:
    name: str
    left: str
    right: str


def part_one(instructions: str, nodes: dict[str, Node]) -> int:
    current = "AAA"
    steps = 0
    while current != "ZZZ":
        direction = instructions[steps % len(instructions)]
        if direction == "L":
            current = nodes[current].left
        elif direction == "R":
            current = nodes[current].right
        steps += 1

    return steps


def part_two(instructions: str, nodes: dict[str, Node]) -> int:
    current_nodes = [name for name in nodes.keys() if name.endswith("A")]

    distances: dict[str, int] = {}
    for node in current_nodes:
        current = node
        steps = 0
        while not current.endswith("Z"):
            direction = instructions[steps % len(instructions)]
            if direction == "L":
                current = nodes[current].left
            elif direction == "R":
                current = nodes[current].right
            steps += 1
        distances[node] = steps

    return math.lcm(*distances.values())


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    instructions = problem_input[0]
    nodes: dict[str, Node] = {}
    for line in problem_input[2:]:
        match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        if match is not None:
            name = match.group(1)
            nodes[name] = Node(name, match.group(2), match.group(3))

    print("Part One: ", part_one(instructions, nodes))
    print("Part Two: ", part_two(instructions, nodes))
