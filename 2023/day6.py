import math
import re

from utils import get_and_cache_input


def ways_to_win(time: int, distance: int) -> int:
    x1 = int((time + math.sqrt(time**2 + 4 * -distance)) / 2)
    x2 = int((time - math.sqrt(time**2 + 4 * -distance)) / 2)
    return x1 - x2


def part_one(problem_input: list[str]) -> int:
    times_and_distances = [
        (int(time), int(distance))
        for (time, distance) in zip(
            problem_input[0].strip("Time:").strip().split(),
            problem_input[1].strip("Distance:").strip().split(),
        )
    ]

    return math.prod(
        ways_to_win(time, distance) for time, distance in times_and_distances
    )


def part_two(problem_input: list[str]) -> int:
    time = int(re.sub(r"\s+", "", problem_input[0].strip("Time:")))
    distance = int(re.sub(r"\s+", "", problem_input[1].strip("Distance:")))

    return ways_to_win(time, distance)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
