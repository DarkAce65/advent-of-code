import statistics
from pathlib import Path


def part_one(crab_positions: list[int]) -> int:
    median = int(statistics.median(crab_positions))

    cost = 0
    for position in crab_positions:
        cost += abs(position - median)

    return cost


def compute_triangular_cost(crab_positions: list[int], alignment: int) -> int:
    cost = 0
    for position in crab_positions:
        diff = abs(position - alignment)
        cost += int(diff * (diff + 1) / 2)

    return cost


def part_two(crab_positions: list[int]) -> int:
    alignment = round(sum(crab_positions) / len(crab_positions))
    best_cost = compute_triangular_cost(crab_positions, alignment)

    while True:
        cost = compute_triangular_cost(crab_positions, alignment - 1)
        if cost > best_cost:
            break

        alignment -= 1
        best_cost = cost

    while True:
        cost = compute_triangular_cost(crab_positions, alignment + 1)
        if cost > best_cost:
            break

        alignment += 1
        best_cost = cost

    return best_cost


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    crab_positions = list(map(int, problem_input[0].split(",")))

    print("Part One: ", part_one(crab_positions))
    print("Part Two: ", part_two(crab_positions))
