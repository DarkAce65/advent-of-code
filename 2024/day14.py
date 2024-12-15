import curses
import re
from collections import defaultdict
from curses import window, wrapper
from math import prod
from typing import Callable, NamedTuple

from utils import get_and_cache_input

CHARACTER_RAMP = " .:-=+*#%@"


class Vector2(NamedTuple):
    x: int
    y: int


class Robot:
    position: Vector2
    velocity: Vector2

    def __init__(self, x: int, y: int, vx: int, vy: int):
        self.position = Vector2(x, y)
        self.velocity = Vector2(vx, vy)

    def get_position(self, t: int, width: int, height: int) -> Vector2:
        return Vector2(
            (self.position.x + self.velocity.x * t) % width,
            (self.position.y + self.velocity.y * t) % height,
        )


def parse_robots(problem_input: list[str]) -> list[Robot]:
    robots: list[Robot] = []
    for row in problem_input:
        match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", row)
        if match is not None:
            x, y, vx, vy = match.groups()
            robots.append(Robot(int(x), int(y), int(vx), int(vy)))
    return robots


def render_robots(
    robots: list[Robot], width: int, height: int
) -> Callable[[window], int]:
    def render(screen: window) -> int:
        nonlocal robots, width, height

        t = 7093

        while True:
            key = screen.getkey()
            if key == "q":
                return t
            elif key == "KEY_RIGHT":
                t += 1
            elif key == "KEY_LEFT":
                t -= 1

            max_y, max_x = screen.getmaxyx()
            max_value = max(width / max_x, height / max_y)
            pixels: dict[Vector2, int] = defaultdict(int)

            screen.clear()
            for robot in robots:
                position = robot.get_position(t, width, height)
                pixels[
                    Vector2(
                        min(int(position.x / width * max_x), max_x),
                        min(int(position.y / height * max_y), max_y),
                    )
                ] += 1

            for pixel, weight in pixels.items():
                try:
                    screen.addch(
                        pixel.y,
                        pixel.x,
                        CHARACTER_RAMP[
                            min(
                                int(weight / max_value * len(CHARACTER_RAMP)),
                                len(CHARACTER_RAMP) - 1,
                            )
                        ],
                    )
                except curses.error:
                    pass

            screen.addstr(0, 0, f"t = {t}")
            screen.refresh()

    return render


def part_one(problem_input: list[str]) -> int:
    robots = parse_robots(problem_input)

    width = 101
    height = 103
    quadrants = [0, 0, 0, 0]

    half_width = int(width / 2)
    half_height = int(height / 2)
    for robot in robots:
        position = robot.get_position(100, width, height)

        if position.y < half_height:
            if position.x < half_width:
                quadrants[0] += 1
            elif position.x > half_width:
                quadrants[1] += 1
        elif position.y > half_height:
            if position.x < half_width:
                quadrants[2] += 1
            elif position.x > half_width:
                quadrants[3] += 1

    return prod(quadrants)


def part_two(problem_input: list[str]) -> int:
    robots = parse_robots(problem_input)

    width = 101
    height = 103

    return wrapper(render_robots(robots, width, height))


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
