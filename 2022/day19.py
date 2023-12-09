import math
import re
from collections import deque
from typing import Literal, Union

from utils import get_and_cache_input

RobotType = Union[Literal["ore"], Literal["clay"], Literal["obsidian"], Literal["geode"]]
ROBOT_TYPES: list[RobotType] = ["ore", "clay", "obsidian", "geode"]


class FactoryBlueprint:
    id: int
    ore_robot_cost: int
    clay_robot_cost: int
    obsidian_robot_cost: tuple[int, int]
    geode_robot_cost: tuple[int, int]

    def __init__(self, blueprint_str: str) -> None:
        match = re.match(
            r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
            blueprint_str,
        )
        if match is None:
            raise ValueError(blueprint_str)

        self.id = int(match.group(1))
        self.ore_robot_cost = int(match.group(2))
        self.clay_robot_cost = int(match.group(3))
        self.obsidian_robot_cost = (int(match.group(4)), int(match.group(5)))
        self.geode_robot_cost = (int(match.group(6)), int(match.group(7)))

    def get_next_state(
        self,
        bot_counts: list[int],
        resource_counts: list[int],
        next_robot_to_build: RobotType,
    ) -> tuple[list[int], list[int], int]:
        new_bot_counts = bot_counts.copy()
        new_resource_counts = resource_counts.copy()
        time_cost = 0
        if next_robot_to_build == "ore":
            time_cost = 1
            if self.ore_robot_cost > resource_counts[0]:
                time_cost += int(
                    math.ceil((self.ore_robot_cost - resource_counts[0]) / bot_counts[0])
                )

            new_resource_counts[0] -= self.ore_robot_cost
            for i in range(len(new_resource_counts)):
                new_resource_counts[i] += bot_counts[i] * time_cost
            new_bot_counts[0] += 1
        elif next_robot_to_build == "clay":
            time_cost = 1
            if self.clay_robot_cost > resource_counts[0]:
                time_cost += int(
                    math.ceil((self.clay_robot_cost - resource_counts[0]) / bot_counts[0])
                )
            new_resource_counts[0] -= self.clay_robot_cost
            for i in range(len(new_resource_counts)):
                new_resource_counts[i] += bot_counts[i] * time_cost
            new_bot_counts[1] += 1
        elif next_robot_to_build == "obsidian":
            ore_time_cost = 0
            clay_time_cost = 0
            if self.obsidian_robot_cost[0] > resource_counts[0]:
                ore_time_cost = int(
                    math.ceil(
                        (self.obsidian_robot_cost[0] - resource_counts[0]) / bot_counts[0]
                    )
                )
            if self.obsidian_robot_cost[1] > resource_counts[1]:
                clay_time_cost = int(
                    math.ceil(
                        (self.obsidian_robot_cost[1] - resource_counts[1]) / bot_counts[1]
                    )
                )
            time_cost = max(ore_time_cost, clay_time_cost) + 1
            new_resource_counts[0] -= self.obsidian_robot_cost[0]
            new_resource_counts[1] -= self.obsidian_robot_cost[1]
            for i in range(len(new_resource_counts)):
                new_resource_counts[i] += bot_counts[i] * time_cost
            new_bot_counts[2] += 1
        elif next_robot_to_build == "geode":
            ore_time_cost = 0
            obsidian_time_cost = 0
            if self.geode_robot_cost[0] > resource_counts[0]:
                ore_time_cost = int(
                    math.ceil(
                        (self.geode_robot_cost[0] - resource_counts[0]) / bot_counts[0]
                    )
                )
            if self.geode_robot_cost[1] > resource_counts[2]:
                obsidian_time_cost = int(
                    math.ceil(
                        (self.geode_robot_cost[1] - resource_counts[2]) / bot_counts[2]
                    )
                )

            time_cost = max(ore_time_cost, obsidian_time_cost) + 1
            new_resource_counts[0] -= self.geode_robot_cost[0]
            new_resource_counts[2] -= self.geode_robot_cost[1]
            for i in range(len(new_resource_counts)):
                new_resource_counts[i] += bot_counts[i] * time_cost
            new_bot_counts[3] += 1
        return (new_bot_counts, new_resource_counts, time_cost)

    def compute_most_geodes_possible(self, total_time: int) -> int:
        possible_states: deque[tuple[list[int], list[int], int]] = deque()
        possible_states.appendleft(([1, 0, 0, 0], [0, 0, 0, 0], 0))

        cache: dict[tuple[tuple[int, int, int, int], tuple[int, int, int, int]], int] = {}
        best_geode_count = 0
        while len(possible_states) > 0:
            bot_counts, resource_counts, time = possible_states.popleft()
            cache_key = (
                (bot_counts[0], bot_counts[1], bot_counts[2], bot_counts[3]),
                (
                    resource_counts[0],
                    resource_counts[1],
                    resource_counts[2],
                    resource_counts[3],
                ),
            )
            if cache_key in cache and cache[cache_key] <= time:
                continue
            cache[cache_key] = time
            for robot_type in ROBOT_TYPES:
                if (
                    (robot_type == "ore" and bot_counts[0] == 0)
                    or (robot_type == "clay" and bot_counts[0] == 0)
                    or (
                        robot_type == "obsidian"
                        and (bot_counts[0] == 0 or bot_counts[1] == 0)
                    )
                    or (
                        robot_type == "geode"
                        and (bot_counts[0] == 0 or bot_counts[2] == 0)
                    )
                ):
                    continue
                if (
                    robot_type == "ore"
                    and resource_counts[0] > self.ore_robot_cost * 2
                    and resource_counts[0] > self.clay_robot_cost * 2
                    and resource_counts[0] > self.obsidian_robot_cost[0] * 2
                    and resource_counts[0] > self.geode_robot_cost[0] * 2
                ):
                    continue
                if (
                    robot_type == "clay"
                    and resource_counts[1] > self.obsidian_robot_cost[1] * 2
                ):
                    continue
                if (
                    robot_type == "obsidian"
                    and resource_counts[2] > self.geode_robot_cost[1] * 2
                ):
                    continue
                if (
                    robot_type != "geode"
                    and self.geode_robot_cost[0] <= resource_counts[0]
                    and self.geode_robot_cost[1] <= resource_counts[2]
                ):
                    continue

                new_bot_counts, new_resource_counts, time_cost = self.get_next_state(
                    bot_counts, resource_counts, robot_type
                )
                if time + time_cost >= total_time:
                    geode_count = resource_counts[3] + (total_time - time) * bot_counts[3]
                    if best_geode_count < geode_count:
                        best_geode_count = geode_count
                    continue

                possible_states.append(
                    (new_bot_counts, new_resource_counts, time + time_cost)
                )

        return best_geode_count


def part_one(problem_input: list[str]) -> int:
    blueprints: list[FactoryBlueprint] = []
    for blueprint_str in problem_input:
        blueprints.append(FactoryBlueprint(blueprint_str))

    return sum(
        blueprint.id * blueprint.compute_most_geodes_possible(24)
        for blueprint in blueprints
    )


def part_two(problem_input: list[str]) -> int:
    blueprints: list[FactoryBlueprint] = []
    for blueprint_str in problem_input[:3]:
        blueprints.append(FactoryBlueprint(blueprint_str))

    return math.prod(
        blueprint.compute_most_geodes_possible(32) for blueprint in blueprints
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
