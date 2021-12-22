from __future__ import annotations

import functools
from pathlib import Path
from typing import Iterable


class Cuboid:
    x_bounds: tuple[int, int]
    y_bounds: tuple[int, int]
    z_bounds: tuple[int, int]

    def __init__(
        self,
        x_bounds: tuple[int, int],
        y_bounds: tuple[int, int],
        z_bounds: tuple[int, int],
    ) -> None:
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.z_bounds = z_bounds

    def compute_volume(self) -> int:
        (x_low, x_high) = self.x_bounds
        (y_low, y_high) = self.y_bounds
        (z_low, z_high) = self.z_bounds

        return (x_high + 1 - x_low) * (y_high + 1 - y_low) * (z_high + 1 - z_low)

    def subtract(self, other: Cuboid) -> list[Cuboid]:
        (x_low, x_high) = self.x_bounds
        (y_low, y_high) = self.y_bounds
        (z_low, z_high) = self.z_bounds

        (x_low_other, x_high_other) = other.x_bounds
        (y_low_other, y_high_other) = other.y_bounds
        (z_low_other, z_high_other) = other.z_bounds

        if (
            x_high < x_low_other
            or x_high_other < x_low
            or y_high < y_low_other
            or y_high_other < y_low
            or z_high < z_low_other
            or z_high_other < z_low
        ):
            return [self]

        split_cuboids: list[Cuboid] = []
        if x_low <= x_low_other - 1:
            split_cuboids.append(
                Cuboid((x_low, x_low_other - 1), (y_low, y_high), (z_low, z_high))
            )
        if x_high_other + 1 <= x_high:
            split_cuboids.append(
                Cuboid((x_high_other + 1, x_high), (y_low, y_high), (z_low, z_high))
            )
        x_low = max(x_low, x_low_other)
        x_high = min(x_high, x_high_other)
        if x_low <= x_high:
            if y_low <= y_low_other - 1:
                split_cuboids.append(
                    Cuboid((x_low, x_high), (y_low, y_low_other - 1), (z_low, z_high))
                )
            if y_high_other + 1 <= y_high:
                split_cuboids.append(
                    Cuboid((x_low, x_high), (y_high_other + 1, y_high), (z_low, z_high))
                )
            y_low = max(y_low, y_low_other)
            y_high = min(y_high, y_high_other)
            if y_low <= y_high:
                if z_low <= z_low_other - 1:
                    split_cuboids.append(
                        Cuboid((x_low, x_high), (y_low, y_high), (z_low, z_low_other - 1))
                    )
                if z_high_other + 1 <= z_high:
                    split_cuboids.append(
                        Cuboid(
                            (x_low, x_high), (y_low, y_high), (z_high_other + 1, z_high)
                        )
                    )

        return split_cuboids


Instruction = tuple[bool, Cuboid]


def clamp(num: int, low: int, high: int) -> int:
    return max(low, min(num, high))


def parse_instructions(problem_input: Iterable[str]) -> list[Instruction]:
    instructions = []
    for instruction in problem_input:
        [state, bounds] = instruction.split()
        [x_bounds, y_bounds, z_bounds] = bounds.split(",")
        [x_low, x_high] = list(map(int, x_bounds[2:].split("..")))
        [y_low, y_high] = list(map(int, y_bounds[2:].split("..")))
        [z_low, z_high] = list(map(int, z_bounds[2:].split("..")))
        instructions.append(
            (
                True if state == "on" else False,
                Cuboid((x_low, x_high), (y_low, y_high), (z_low, z_high)),
            )
        )

    return instructions


def part_one(instructions: list[Instruction]) -> int:
    enabled_cubes: set[tuple[int, int, int]] = set()
    for (should_enable, cuboid) in instructions:
        (x_low, x_high) = cuboid.x_bounds
        (y_low, y_high) = cuboid.y_bounds
        (z_low, z_high) = cuboid.z_bounds
        if (
            x_high < -50
            or 50 < x_low
            or y_high < -50
            or 50 < y_low
            or z_high < -50
            or 50 < z_low
        ):
            continue

        (x_low, x_high) = (clamp(x_low, -50, 50), clamp(x_high, -50, 50))
        (y_low, y_high) = (clamp(y_low, -50, 50), clamp(y_high, -50, 50))
        (z_low, z_high) = (clamp(z_low, -50, 50), clamp(z_high, -50, 50))

        for x in range(x_low, x_high + 1):
            for y in range(y_low, y_high + 1):
                for z in range(z_low, z_high + 1):
                    if should_enable:
                        enabled_cubes.add((x, y, z))
                    else:
                        if (x, y, z) in enabled_cubes:
                            enabled_cubes.remove((x, y, z))

    return len(enabled_cubes)


def part_two(instructions: list[Instruction]) -> int:
    enabled_cuboids: list[Cuboid] = []
    for (should_enable, cuboid) in instructions:
        if should_enable:
            cuboids_to_add = [cuboid]
            for enabled_cuboid in enabled_cuboids:
                cuboids_to_add = functools.reduce(
                    lambda cuboids, c: cuboids + c.subtract(enabled_cuboid),
                    cuboids_to_add,
                    [],
                )
            enabled_cuboids = enabled_cuboids + cuboids_to_add
        else:
            enabled_cuboids = functools.reduce(
                lambda cuboids, c: cuboids + c.subtract(cuboid), enabled_cuboids, []
            )

    return sum(map(lambda cuboid: cuboid.compute_volume(), enabled_cuboids))


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    instructions = parse_instructions(filter(None, problem_input))

    print("Part One: ", part_one(instructions))
    print("Part Two: ", part_two(instructions))
