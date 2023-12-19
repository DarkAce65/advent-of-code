from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from utils import get_and_cache_input


@dataclass(frozen=True)
class Rating:
    x: int
    m: int
    a: int
    s: int

    def get_sum(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass(frozen=True)
class RatingBand:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def get(self, category: str) -> tuple[int, int]:
        if category == "x":
            return self.x
        elif category == "m":
            return self.m
        elif category == "a":
            return self.a
        elif category == "s":
            return self.s
        raise ValueError("Unknown category")

    def is_in_band(self, category: str, value: int) -> bool:
        return self.get(category)[0] <= value <= self.get(category)[1]

    def split(self, category: str, value: int) -> tuple[RatingBand, RatingBand]:
        assert self.is_in_band(category, value)

        if category == "x":
            return (
                RatingBand((self.x[0], value - 1), self.m, self.a, self.s),
                RatingBand((value, self.x[1]), self.m, self.a, self.s),
            )
        elif category == "m":
            return (
                RatingBand(self.x, (self.m[0], value - 1), self.a, self.s),
                RatingBand(self.x, (value, self.m[1]), self.a, self.s),
            )
        elif category == "a":
            return (
                RatingBand(self.x, self.m, (self.a[0], value - 1), self.s),
                RatingBand(self.x, self.m, (value, self.a[1]), self.s),
            )
        elif category == "s":
            return (
                RatingBand(self.x, self.m, self.a, (self.s[0], value - 1)),
                RatingBand(self.x, self.m, self.a, (value, self.s[1])),
            )
        raise ValueError("Unknown category")

    def count_combinations(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )


@dataclass
class Workflow:
    steps: list[tuple[str, Optional[str]]]

    def evaluate_condition(self, condition: str, rating: Rating) -> bool:
        replaced_condition = (
            condition.replace("x", str(rating.x))
            .replace("m", str(rating.m))
            .replace("a", str(rating.a))
            .replace("s", str(rating.s))
        )
        return eval(replaced_condition)

    def evaluate(self, rating: Rating) -> str:
        for result, condition in self.steps:
            if condition is None or self.evaluate_condition(condition, rating):
                return result

        raise ValueError("Couldn't evaluate workflow")


def make_workflow(steps: list[str]) -> Workflow:
    parsed_steps: list[tuple[str, Optional[str]]] = []
    for step in steps:
        if ":" in step:
            condition, result = step.split(":")
            parsed_steps.append((result, condition))
        else:
            parsed_steps.append((step, None))

    return Workflow(parsed_steps)


def part_one(workflows: dict[str, Workflow], ratings: list[Rating]) -> int:
    result = 0
    for rating in ratings:
        part_result = "in"
        while part_result != "A" and part_result != "R":
            part_result = workflows[part_result].evaluate(rating)
        if part_result == "A":
            result += rating.get_sum()

    return result


def count_accepted_combinations(
    workflows: dict[str, Workflow], band: RatingBand, workflow_name: str, index: int
) -> int:
    step_result, step_condition = workflows[workflow_name].steps[index]
    if step_condition is None:
        if step_result == "A":
            return band.count_combinations()
        elif step_result == "R":
            return 0
        else:
            return count_accepted_combinations(workflows, band, step_result, 0)

    category_and_value = re.split(r"[<>]", step_condition)
    category, value = category_and_value[0], int(category_and_value[1])

    if "<" in step_condition:
        if band.get(category)[1] < value:
            if step_result == "A":
                return band.count_combinations()
            elif step_result == "R":
                return 0
            else:
                return count_accepted_combinations(workflows, band, step_result, 0)
        elif band.get(category)[0] >= value:
            return count_accepted_combinations(workflows, band, workflow_name, index + 1)
        else:
            combinations = 0
            band_low, band_high = band.split(category, value)
            if step_result == "A":
                combinations += band_low.count_combinations()
            elif step_result != "R":
                combinations += count_accepted_combinations(
                    workflows, band_low, step_result, 0
                )
            combinations += count_accepted_combinations(
                workflows, band_high, workflow_name, index + 1
            )
            return combinations
    elif ">" in step_condition:
        if band.get(category)[0] > value:
            if step_result == "A":
                return band.count_combinations()
            elif step_result == "R":
                return 0
            else:
                return count_accepted_combinations(workflows, band, step_result, 0)
        elif band.get(category)[1] <= value:
            return count_accepted_combinations(workflows, band, workflow_name, index + 1)
        else:
            combinations = 0
            band_low, band_high = band.split(category, value + 1)
            combinations += count_accepted_combinations(
                workflows, band_low, workflow_name, index + 1
            )
            if step_result == "A":
                combinations += band_high.count_combinations()
            elif step_result != "R":
                combinations += count_accepted_combinations(
                    workflows, band_high, step_result, 0
                )
            return combinations

    raise ValueError("Invalid condition")


def part_two(workflows: dict[str, Workflow]) -> int:
    return count_accepted_combinations(
        workflows, RatingBand((1, 4000), (1, 4000), (1, 4000), (1, 4000)), "in", 0
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    workflows: dict[str, Workflow] = {}
    ratings: list[Rating] = []
    is_workflows = True
    for line in problem_input:
        if len(line) == 0:
            is_workflows = False
        elif is_workflows:
            match = re.match(r"([a-z]+)\{([^{}]+)\}", line)
            assert match is not None
            workflow_name, steps = match.group(1), match.group(2).split(",")
            workflows[workflow_name] = make_workflow(steps)
        else:
            match = re.match(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", line)
            assert match is not None
            ratings.append(
                Rating(
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3)),
                    int(match.group(4)),
                )
            )

    print("Part One: ", part_one(workflows, ratings))
    print("Part Two: ", part_two(workflows))
