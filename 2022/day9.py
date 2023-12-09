import math

from utils import get_and_cache_input


def are_touching(head: list[int], tail: list[int]) -> bool:
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1


def part_one(problem_input: list[str]) -> int:
    head = [0, 0]
    tail = [0, 0]
    visited_positions: set[str] = set()

    visited_positions.add(f"{tail[0]},{tail[1]}")
    for action in problem_input:
        dir, dist_str = action.split(" ")
        dist = int(dist_str)
        for _ in range(dist):
            if dir == "U":
                head[1] += 1
            elif dir == "R":
                head[0] += 1
            elif dir == "D":
                head[1] -= 1
            elif dir == "L":
                head[0] -= 1

            if not are_touching(head, tail):
                if head[0] - tail[0] != 0:
                    tail[0] += int(math.copysign(1, head[0] - tail[0]))
                if head[1] - tail[1] != 0:
                    tail[1] += int(math.copysign(1, head[1] - tail[1]))

            visited_positions.add(f"{tail[0]},{tail[1]}")

    return len(visited_positions)


def part_two(problem_input: list[str]) -> int:
    rope = [[0, 0] for _ in range(10)]
    visited_positions: set[str] = set()

    visited_positions.add(f"{rope[-1][0]},{rope[-1][1]}")
    for action in problem_input:
        dir, dist_str = action.split(" ")
        dist = int(dist_str)
        for _ in range(dist):
            if dir == "U":
                rope[0][1] += 1
            elif dir == "R":
                rope[0][0] += 1
            elif dir == "D":
                rope[0][1] -= 1
            elif dir == "L":
                rope[0][0] -= 1

            for i, knot in enumerate(rope):
                if i == 0:
                    continue

                knot_before = rope[i - 1]
                if not are_touching(knot_before, knot):
                    if knot_before[0] - knot[0] != 0:
                        knot[0] += int(math.copysign(1, knot_before[0] - knot[0]))
                    if knot_before[1] - knot[1] != 0:
                        knot[1] += int(math.copysign(1, knot_before[1] - knot[1]))

            visited_positions.add(f"{rope[-1][0]},{rope[-1][1]}")

    return len(visited_positions)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
