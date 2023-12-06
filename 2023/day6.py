import math
import re
from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    times_and_distances = [
        (int(time), int(distance))
        for (time, distance) in zip(
            problem_input[0].strip("Time:").strip().split(),
            problem_input[1].strip("Distance:").strip().split(),
        )
    ]

    ways_to_win = []
    for time, distance in times_and_distances:
        ways_to_win.append(0)
        for charge_time in range(time):
            if charge_time * (time - charge_time) > distance:
                ways_to_win[-1] += 1

    return math.prod(ways_to_win)


def part_two(problem_input: list[str]) -> int:
    time = int(re.sub(r"\s+", "", problem_input[0].strip("Time:")))
    distance = int(re.sub(r"\s+", "", problem_input[1].strip("Distance:")))

    ways_to_win = 0
    for charge_time in range(time):
        if charge_time * (time - charge_time) > distance:
            ways_to_win += 1

    return ways_to_win


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
