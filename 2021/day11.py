import copy

from utils import get_and_cache_input


def ripple(energy_levels: list[list[int]], row: int, col: int) -> None:
    for r in range(max(0, row - 1), min(row + 2, len(energy_levels))):
        for c in range(max(0, col - 1), min(col + 2, len(energy_levels[r]))):
            if energy_levels[r][c] == -1:
                continue

            energy_levels[r][c] += 1
            if energy_levels[r][c] > 9:
                energy_levels[r][c] = -1
                ripple(energy_levels, r, c)


def step(energy_levels: list[list[int]]) -> int:
    num_flashes = 0
    for row in range(len(energy_levels)):
        for col in range(len(energy_levels[row])):
            if energy_levels[row][col] == -1:
                continue

            energy_levels[row][col] += 1
            if energy_levels[row][col] > 9:
                energy_levels[row][col] = -1
                ripple(energy_levels, row, col)

    for row in range(len(energy_levels)):
        for col in range(len(energy_levels[row])):
            if energy_levels[row][col] == -1 or energy_levels[row][col] > 9:
                num_flashes += 1
                energy_levels[row][col] = 0

    return num_flashes


def part_one(initial_energy_levels: list[list[int]]) -> int:
    return sum(step(initial_energy_levels) for _ in range(100))


def part_two(initial_energy_levels: list[list[int]]) -> int:
    step_number = 0
    num_octopuses = len(initial_energy_levels) * len(initial_energy_levels[0])

    while True:
        num_flashes = step(initial_energy_levels)
        step_number += 1
        if num_flashes == num_octopuses:
            return step_number


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    initial_energy_levels = [list(map(int, row)) for row in problem_input]

    print("Part One: ", part_one(copy.deepcopy(initial_energy_levels)))
    print("Part Two: ", part_two(copy.deepcopy(initial_energy_levels)))
