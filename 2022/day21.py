from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from utils import get_and_cache_input


def resolve_monkey(
    monkey: str,
    monkey_equations: dict[str, tuple[str, str, str] | int],
    cache: dict[str, int] | None = None,
) -> int:
    if cache is None:
        cache = {}

    if monkey in cache:
        return cache[monkey]

    if monkey in monkey_equations:
        expression = monkey_equations[monkey]
        if isinstance(expression, int):
            cache[monkey] = expression
            return expression
        else:
            left, operator, right = expression
            resolved_left = resolve_monkey(left, monkey_equations, cache)
            resolved_right = resolve_monkey(right, monkey_equations, cache)
            if operator == "+":
                resolved_value = resolved_left + resolved_right
            elif operator == "-":
                resolved_value = resolved_left - resolved_right
            elif operator == "*":
                resolved_value = resolved_left * resolved_right
            elif operator == "/":
                resolved_value = int(resolved_left / resolved_right)
            else:
                raise ValueError("Unrecognized operator `" + operator + "`")

            cache[monkey] = resolved_value
            return resolved_value

    raise ValueError("Cannot solve monkey `" + monkey + "`")


@dataclass
class Expression:
    left: Expression | Literal["humn"] | int
    right: Expression | Literal["humn"] | int
    operator: str

    def __repr__(self) -> str:
        return "(" + str(self.left) + " " + self.operator + " " + str(self.right) + ")"


def build_tree(
    monkey: str,
    monkey_equations: dict[str, tuple[str, str, str] | int],
    cache: dict[str, Expression | Literal["humn"] | int] | None = None,
) -> Expression | Literal["humn"] | int:
    if cache is None:
        cache = {}

    if monkey in cache:
        return cache[monkey]

    if monkey == "humn":
        return "humn"
    elif monkey in monkey_equations:
        expression = monkey_equations[monkey]
        if isinstance(expression, int):
            cache[monkey] = expression
            return expression
        else:
            left, operator, right = expression
            resolved_left = build_tree(left, monkey_equations, cache)
            resolved_right = build_tree(right, monkey_equations, cache)
            resolved_value: Expression | Literal["humn"] | int
            if isinstance(resolved_left, int) and isinstance(resolved_right, int):
                if operator == "+":
                    resolved_value = resolved_left + resolved_right
                elif operator == "-":
                    resolved_value = resolved_left - resolved_right
                elif operator == "*":
                    resolved_value = resolved_left * resolved_right
                elif operator == "/":
                    resolved_value = int(resolved_left / resolved_right)
                else:
                    raise ValueError("Unrecognized operator `" + operator + "`")
            else:
                resolved_value = Expression(
                    left=resolved_left, right=resolved_right, operator=operator
                )

            cache[monkey] = resolved_value
            return resolved_value

    raise ValueError("Cannot solve monkey `" + monkey + "`")


def solve_for_humn(humn_exp: Expression | Literal["humn"], value: int) -> int:
    while humn_exp != "humn":
        if isinstance(humn_exp.left, int) and not isinstance(humn_exp.right, int):
            if humn_exp.operator == "+":
                value -= humn_exp.left
            elif humn_exp.operator == "-":
                value = humn_exp.left - value
            elif humn_exp.operator == "*":
                value = int(value / humn_exp.left)
            elif humn_exp.operator == "/":
                value = int(humn_exp.left / value)
            humn_exp = humn_exp.right
        elif isinstance(humn_exp.right, int) and not isinstance(humn_exp.left, int):
            if humn_exp.operator == "+":
                value -= humn_exp.right
            elif humn_exp.operator == "-":
                value += humn_exp.right
            elif humn_exp.operator == "*":
                value = int(value / humn_exp.right)
            elif humn_exp.operator == "/":
                value *= humn_exp.right
            humn_exp = humn_exp.left
        else:
            raise ValueError

    return value


def part_one(problem_input: list[str]) -> int:
    monkey_equations: dict[str, tuple[str, str, str] | int] = {}
    for line in problem_input:
        match = re.match(r"(\w+): (\-?\d+)", line)
        if match is not None:
            monkey = match.group(1)
            value = int(match.group(2))
            monkey_equations[monkey] = value
            continue
        match = re.match(r"(\w+): (\w+) ([+\-*/]) (\w+)", line)
        if match is not None:
            monkey = match.group(1)
            left = match.group(2)
            operator = match.group(3)
            right = match.group(4)
            monkey_equations[monkey] = (left, operator, right)
            continue

    return resolve_monkey("root", monkey_equations)


def part_two(problem_input: list[str]) -> int:
    monkey_equations: dict[str, tuple[str, str, str] | int] = {}
    left_monkey = ""
    right_monkey = ""
    for line in problem_input:
        match = re.match(r"(\w+): (\-?\d+)", line)
        if match is not None:
            monkey = match.group(1)
            if monkey == "humn":
                continue
            value = int(match.group(2))
            monkey_equations[monkey] = value
            continue
        match = re.match(r"(\w+): (\w+) ([+\-*/]) (\w+)", line)
        if match is not None:
            monkey = match.group(1)
            if monkey == "humn":
                continue
            left = match.group(2)
            operator = match.group(3)
            right = match.group(4)
            if monkey == "root":
                left_monkey = left
                right_monkey = right
                continue
            monkey_equations[monkey] = (left, operator, right)
            continue

    expression_1 = build_tree(left_monkey, monkey_equations)
    expression_2 = build_tree(right_monkey, monkey_equations)

    if isinstance(expression_1, Expression) and isinstance(expression_2, int):
        return solve_for_humn(expression_1, expression_2)
    elif isinstance(expression_1, int) and isinstance(expression_2, Expression):
        return solve_for_humn(expression_2, expression_1)

    raise NotImplementedError


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
