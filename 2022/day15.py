import re

from utils import get_and_cache_input

Position = tuple[int, int]


def manhattan_distance(from_pos: Position, to_pos: Position) -> int:
    return abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1])


def parse_sensor_and_beacon(input: str) -> tuple[Position, Position]:
    match = re.match(
        r"Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)",
        input,
    )
    if match is None:
        raise ValueError(f"Failed to parse input `{input}`")

    sensor = (int(match.group(1)), int(match.group(2)))
    beacon = (int(match.group(3)), int(match.group(4)))

    return (sensor, beacon)


def part_one(problem_input: list[str]) -> int:
    target_y = 2_000_000

    cannot_be_beacon: set[Position] = set()
    for line in problem_input:
        sensor, beacon = parse_sensor_and_beacon(line)
        dist = manhattan_distance(sensor, beacon)

        for i in range(sensor[0] - dist, sensor[0] + dist + 1):
            if (i, target_y) == beacon:
                if beacon in cannot_be_beacon:
                    cannot_be_beacon.remove(beacon)
                continue
            if manhattan_distance(sensor, (i, target_y)) <= dist:
                cannot_be_beacon.add((i, target_y))

    return len(cannot_be_beacon)


def can_combine_ranges(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    return (
        (range1[0] - 1 <= range2[0] and range2[0] <= range1[1] + 1)
        or (range1[0] - 1 <= range2[1] and range2[1] <= range1[1] + 1)
        or (range2[0] <= range1[0] and range1[1] <= range2[1])
    )


def combine_ranges(range1: tuple[int, int], range2: tuple[int, int]) -> tuple[int, int]:
    return (
        min(range1[0], range1[1], range2[0], range2[1]),
        max(range1[0], range1[1], range2[0], range2[1]),
    )


class Ranges:
    ranges: list[tuple[int, int]]

    def __init__(self) -> None:
        self.ranges = []

    def add_range(self, new_range: tuple[int, int]):
        assert new_range[0] <= new_range[1], new_range
        did_combine_ranges = False
        for i, r in enumerate(self.ranges):
            if can_combine_ranges(r, new_range):
                old_range = self.ranges.pop(i)
                self.add_range(combine_ranges(old_range, new_range))
                did_combine_ranges = True
                break

        if not did_combine_ranges:
            self.ranges.append(new_range)

    def find_containing_range(self, num: int) -> tuple[int, int] | None:
        for r in self.ranges:
            if r[0] <= num and num <= r[1]:
                return r

        return None

    def __repr__(self) -> str:
        return str(self.ranges)


def part_two(problem_input: list[str]) -> int:
    coordinate_bounds = 4_000_000

    sensor_ranges_to_skip: dict[int, Ranges] = {}

    for i, line in enumerate(problem_input):
        sensor, beacon = parse_sensor_and_beacon(line)
        print(f"[{i + 1}/{len(problem_input)}] Building ranges for {sensor}")
        dist = manhattan_distance(sensor, beacon)
        for y in range(sensor[1] - dist, sensor[1] + dist + 1):
            if y < 0 or coordinate_bounds < y:
                continue

            x_low = sensor[0] - (dist - abs(sensor[1] - y))
            x_high = sensor[0] + (dist - abs(sensor[1] - y))
            if x_high < 0 or coordinate_bounds < x_low:
                continue

            if y not in sensor_ranges_to_skip:
                sensor_ranges_to_skip[y] = Ranges()
            new_range = (max(0, x_low), min(x_high, coordinate_bounds))
            sensor_ranges_to_skip[y].add_range(new_range)

    print("Finding distress beacon...")
    for y in range(coordinate_bounds + 1):
        x = 0
        while x <= coordinate_bounds:
            if y not in sensor_ranges_to_skip:
                return x * 4_000_000 + y
            containing_range = sensor_ranges_to_skip[y].find_containing_range(x)
            if containing_range is None:
                return x * 4_000_000 + y

            x = containing_range[1] + 1

    raise ValueError("Couldn't find distress beacon")


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    # print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
