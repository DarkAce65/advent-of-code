from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeGuard, TypeVar, cast


class divisibleint:
    remainders: dict[int, int]

    def __init__(self, remainders: dict[int, int]) -> None:
        self.remainders = remainders

    @classmethod
    def for_divisors(cls, x: int, divisors: list[int]) -> divisibleint:
        d = cls({})
        for divisor in divisors:
            d.remainders[divisor] = x % divisor
        return d

    def copy(self) -> divisibleint:
        return divisibleint(self.remainders.copy())

    def is_divisible_by(self, x: int) -> bool:
        if x not in self.remainders:
            raise ValueError(f"Unknown divisor `{x}`")
        return self.remainders[x] == 0

    def add(self, x: int) -> divisibleint:
        d = self.copy()
        for divisor in d.remainders.keys():
            d.remainders[divisor] = (d.remainders[divisor] + x) % divisor
        return d

    def multiply(self, x: int) -> divisibleint:
        d = self.copy()
        for divisor in d.remainders.keys():
            d.remainders[divisor] = (d.remainders[divisor] * x) % divisor
        return d

    def square(self) -> divisibleint:
        d = self.copy()
        for divisor in d.remainders.keys():
            d.remainders[divisor] = (
                d.remainders[divisor] * d.remainders[divisor]
            ) % divisor
        return d

    def __str__(self) -> str:
        return str(self.remainders)

    def __repr__(self) -> str:
        return str(self.remainders)


T = TypeVar("T")


@dataclass
class ThrownItem(Generic[T]):
    item: T
    to_index: int


def is_int_list(lst: list[int] | list[divisibleint]) -> TypeGuard[list[int]]:
    return len(lst) == 0 or isinstance(lst[0], int)


def is_divisibleint_list(
    lst: list[int] | list[divisibleint],
) -> TypeGuard[list[divisibleint]]:
    return len(lst) == 0 or isinstance(lst[0], divisibleint)


class Monkey:
    items: list[int] | list[divisibleint]
    equation: str
    test_divisible_by: int
    if_true_index: int
    if_false_index: int

    inspected_items: int

    def __init__(
        self,
        starting_items: list[int],
        equation: str,
        test_divisible_by: int,
        if_true_index: int,
        if_false_index: int,
        divisors: list[int],
        use_divisible_int: bool = False,
    ) -> None:
        self.items = (
            [divisibleint.for_divisors(x, divisors) for x in starting_items]
            if use_divisible_int
            else starting_items
        )
        self.equation = equation
        self.test_divisible_by = test_divisible_by
        self.if_true_index = if_true_index
        self.if_false_index = if_false_index

        self.inspected_items = 0

    def operation_bounded(self, x: int) -> int:
        if "+" in self.equation:
            return x + int(self.equation.split("+")[1].strip())
        elif "*" in self.equation:
            multiplicand = self.equation.split("*")[1].strip()
            if multiplicand == "old":
                return x * x
            else:
                return x * int(multiplicand)

        raise ValueError(f"Unknown operation `{self.equation}`")

    def operation(self, x: divisibleint) -> divisibleint:
        if "+" in self.equation:
            return x.add(int(self.equation.split("+")[1].strip()))
        elif "*" in self.equation:
            multiplicand = self.equation.split("*")[1].strip()
            if multiplicand == "old":
                return x.square()
            else:
                return x.multiply(int(multiplicand))

        raise ValueError(f"Unknown operation `{self.equation}`")

    def throw_items_bounded(self) -> list[ThrownItem[int]]:
        if not is_int_list(self.items):
            raise ValueError

        thrown_items: list[ThrownItem[int]] = []
        for i in range(len(self.items)):
            self.items[i] = int(self.operation_bounded(self.items[i]) / 3)
            thrown_items.append(
                ThrownItem(
                    self.items[i],
                    self.if_true_index
                    if self.items[i] % self.test_divisible_by == 0
                    else self.if_false_index,
                )
            )

            self.inspected_items += 1

        self.items = cast(list[int], [])

        return thrown_items

    def throw_items(self) -> list[ThrownItem[divisibleint]]:
        if not is_divisibleint_list(self.items):
            raise ValueError

        thrown_items: list[ThrownItem[divisibleint]] = []
        for i in range(len(self.items)):
            self.items[i] = self.operation(self.items[i])
            thrown_items.append(
                ThrownItem(
                    self.items[i],
                    self.if_true_index
                    if self.items[i].is_divisible_by(self.test_divisible_by)
                    else self.if_false_index,
                )
            )

            self.inspected_items += 1

        self.items = cast(list[divisibleint], [])

        return thrown_items


def parse_monkeys(problem_input: list[str], *, use_divisible_int=False) -> list[Monkey]:
    divisors: list[int] = []
    for line in problem_input:
        if "Test: divisible by " in line:
            divisors.append(int(line.strip().removeprefix("Test: divisible by ")))

    monkeys: list[Monkey] = []
    i = 0
    while i < len(problem_input):
        if problem_input[i].startswith("Monkey"):
            starting_items = [
                int(item.strip())
                for item in problem_input[i + 1]
                .strip()
                .removeprefix("Starting items: ")
                .split(",")
            ]
            equation = problem_input[i + 2].strip().removeprefix("Operation: new = ")
            test_divisible_by = int(
                problem_input[i + 3].strip().removeprefix("Test: divisible by ")
            )
            if_true_index = int(
                problem_input[i + 4].strip().removeprefix("If true: throw to monkey ")
            )
            if_false_index = int(
                problem_input[i + 5].strip().removeprefix("If false: throw to monkey ")
            )
            monkeys.append(
                Monkey(
                    starting_items,
                    equation,
                    test_divisible_by,
                    if_true_index,
                    if_false_index,
                    divisors,
                    use_divisible_int,
                )
            )

            i += 6
        else:
            i += 1

    return monkeys


def part_one(problem_input: list[str]) -> int:
    monkeys = parse_monkeys(problem_input)

    for _ in range(20):
        for monkey in monkeys:
            thrown_items = monkey.throw_items_bounded()
            for thrown_item in thrown_items:
                target_list = monkeys[thrown_item.to_index].items
                if not is_int_list(target_list):
                    raise ValueError
                target_list.append(thrown_item.item)

    return math.prod(
        sorted((monkey.inspected_items for monkey in monkeys), reverse=True)[:2]
    )


def part_two(problem_input: list[str]) -> int:
    monkeys = parse_monkeys(problem_input, use_divisible_int=True)

    for _ in range(10000):
        for monkey in monkeys:
            thrown_items = monkey.throw_items()
            for thrown_item in thrown_items:
                target_list = monkeys[thrown_item.to_index].items
                if not is_divisibleint_list(target_list):
                    raise ValueError
                target_list.append(thrown_item.item)

    return math.prod(
        sorted((monkey.inspected_items for monkey in monkeys), reverse=True)[:2]
    )


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
