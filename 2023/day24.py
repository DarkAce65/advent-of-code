from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, NamedTuple

from sympy import Symbol, nonlinsolve, symbols
from utils import get_and_cache_input


class Vector3(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class Hailstone:
    position: Vector3
    velocity: Vector3

    def get_position_at_t(self, t: int) -> Vector3:
        return Vector3(
            self.position.x + self.velocity.x * t,
            self.position.y + self.velocity.y * t,
            self.position.z + self.velocity.z * t,
        )

    def is_value_in_the_past(
        self, dimension: Literal["x", "y", "z"], value: float
    ) -> bool:
        if dimension == "x":
            return (self.velocity.x >= 0 and value < self.position.x) or (
                self.velocity.x < 0 and self.position.x < value
            )
        elif dimension == "y":
            return (self.velocity.y >= 0 and value < self.position.y) or (
                self.velocity.y < 0 and self.position.y < value
            )
        elif dimension == "z":
            return (self.velocity.z >= 0 and value < self.position.z) or (
                self.velocity.z < 0 and self.position.z < value
            )

    def could_intersect_in_xy_test_area(
        self, other: Hailstone, test_area: tuple[int, int]
    ) -> bool:
        slope = self.velocity.y / self.velocity.x
        other_slope = other.velocity.y / other.velocity.x
        if slope == other_slope:
            return False

        x = (
            slope * self.position.x
            - other_slope * other.position.x
            - self.position.y
            + other.position.y
        ) / (slope - other_slope)
        if (
            test_area[0] <= x <= test_area[1]
            and not self.is_value_in_the_past("x", x)
            and not other.is_value_in_the_past("x", x)
        ):
            y = slope * (x - self.position.x) + self.position.y
            return (
                test_area[0] <= y <= test_area[1]
                and not self.is_value_in_the_past("y", y)
                and not other.is_value_in_the_past("y", y)
            )

        return False

    def make_equation(
        self,
        px: Symbol,
        py: Symbol,
        pz: Symbol,
        vx: Symbol,
        vy: Symbol,
        vz: Symbol,
        t: Symbol,
    ):
        return [
            px + vx * t - (self.position.x + self.velocity.x * t),
            py + vy * t - (self.position.y + self.velocity.y * t),
            pz + vz * t - (self.position.z + self.velocity.z * t),
        ]


def part_one(hailstones: list[Hailstone]) -> int:
    intersections = 0
    for index, hailstone1 in enumerate(hailstones):
        for hailstone2 in hailstones[index + 1 :]:
            if hailstone1.could_intersect_in_xy_test_area(
                hailstone2, (200000000000000, 400000000000000)
            ):
                intersections += 1
    return intersections


def part_two(hailstones: list[Hailstone]) -> int:
    equations = []
    variables = symbols("px, py, pz, vx, vy, vz, t0, t1, t2")
    px, py, pz, vx, vy, vz, t0, t1, t2 = variables

    equations.extend(hailstones[0].make_equation(px, py, pz, vx, vy, vz, t0))
    equations.extend(hailstones[1].make_equation(px, py, pz, vx, vy, vz, t1))
    equations.extend(hailstones[2].make_equation(px, py, pz, vx, vy, vz, t2))

    solutions = list(nonlinsolve(equations, variables))
    assert len(solutions) == 1

    solution = {
        (variable.name): value
        for variable, value in zip(variables, next(iter(solutions)))
    }

    return solution["px"] + solution["py"] + solution["pz"]


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    hailstones: list[Hailstone] = []
    for line in problem_input:
        positions, velocities = line.split("@")
        position = Vector3(*(int(v) for v in positions.split(",")))
        velocity = Vector3(*(int(v) for v in velocities.split(",")))
        hailstones.append(Hailstone(position, velocity))

    print("Part One: ", part_one(hailstones))
    print("Part Two: ", part_two(hailstones))
