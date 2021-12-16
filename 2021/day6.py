from collections import defaultdict
from pathlib import Path


def part_one(initial_state: list[int]) -> int:
    fish_timers = initial_state.copy()

    for _ in range(80):
        num_fish = len(fish_timers)
        for f in range(num_fish):
            fish_timers[f] -= 1
            if fish_timers[f] < 0:
                fish_timers[f] = 6
                fish_timers.append(8)

    return len(fish_timers)


def part_two(initial_state: list[int]) -> int:
    fish_timers: dict[int, int] = defaultdict(int)
    for time in initial_state:
        fish_timers[time] += 1

    for _ in range(256):
        next_fish_timers = fish_timers.copy()
        for time, num_fish in fish_timers.items():
            if time == 0:
                next_fish_timers[time] -= num_fish
                next_fish_timers[6] += num_fish
                next_fish_timers[8] += num_fish
            else:
                next_fish_timers[time] -= num_fish
                next_fish_timers[time - 1] += num_fish

        fish_timers = next_fish_timers

    return sum(list(fish_timers.values()))


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    fish_timers = list(map(int, problem_input[0].split(",")))

    print("Part One: ", part_one(fish_timers))
    print("Part Two: ", part_two(fish_timers))
