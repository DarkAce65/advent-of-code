import time
from pathlib import Path

Position = tuple[int, int]


def get_proposed_location(
    elf: Position, elves: set[Position], offset=0
) -> Position | None:
    elf_to_north = False
    elf_to_south = False
    elf_to_west = False
    elf_to_east = False
    if (
        (elf[0] - 1, elf[1] - 1) in elves
        or (elf[0], elf[1] - 1) in elves
        or (elf[0] + 1, elf[1] - 1) in elves
    ):
        elf_to_north = True
    if (
        (elf[0] - 1, elf[1] + 1) in elves
        or (elf[0], elf[1] + 1) in elves
        or (elf[0] + 1, elf[1] + 1) in elves
    ):
        elf_to_south = True
    if (
        (elf[0] - 1, elf[1] - 1) in elves
        or (elf[0] - 1, elf[1]) in elves
        or (elf[0] - 1, elf[1] + 1) in elves
    ):
        elf_to_west = True
    if (
        (elf[0] + 1, elf[1] - 1) in elves
        or (elf[0] + 1, elf[1]) in elves
        or (elf[0] + 1, elf[1] + 1) in elves
    ):
        elf_to_east = True

    if not elf_to_north and not elf_to_south and not elf_to_west and not elf_to_east:
        return None

    direction_order = ["N", "S", "W", "E"]
    elf_positions = [elf_to_north, elf_to_south, elf_to_west, elf_to_east]
    for i in range(4):
        index = (i + offset) % 4
        if not elf_positions[index]:
            direction = direction_order[index]
            if direction == "N":
                return (elf[0], elf[1] - 1)
            elif direction == "S":
                return (elf[0], elf[1] + 1)
            elif direction == "W":
                return (elf[0] - 1, elf[1])
            elif direction == "E":
                return (elf[0] + 1, elf[1])

    return None


def run_round(elves: set[Position], offset=0) -> set[Position] | None:
    elf_to_next: dict[Position, Position] = {}
    next_to_elf: dict[Position, Position] = {}

    moved_elves: set[Position] = set()

    for elf in elves:
        proposed_location = get_proposed_location(elf, elves, offset)
        if proposed_location is not None:
            if proposed_location in next_to_elf:
                elf_to_next[elf] = elf

                elf_to_next[next_to_elf[proposed_location]] = next_to_elf[
                    proposed_location
                ]
                moved_elves.remove(next_to_elf[proposed_location])
            else:
                elf_to_next[elf] = proposed_location
                next_to_elf[proposed_location] = elf
                moved_elves.add(elf)
        else:
            elf_to_next[elf] = elf

    if len(moved_elves) == 0:
        return None

    return set(elf_to_next.values())


def print_map(elves: set[Position]):
    for y in range(min(elf[1] for elf in elves), max(elf[1] for elf in elves) + 1):
        row = ""
        for x in range(min(elf[0] for elf in elves), max(elf[0] for elf in elves) + 1):
            if (x, y) in elves:
                row += "#"
            else:
                row += "."
        print(row)


def part_one(problem_input: list[str]) -> int:
    elves: set[Position] = set()
    for y, line in enumerate(problem_input):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))

    round_index = 0
    is_done = False
    while not is_done and round_index < 10:
        next_elves = run_round(elves, round_index)
        if next_elves is None:
            is_done = True
            break
        elves = next_elves
        round_index += 1

    width = max(elf[0] for elf in elves) - min(elf[0] for elf in elves) + 1
    height = max(elf[1] for elf in elves) - min(elf[1] for elf in elves) + 1
    return width * height - len(elves)


def part_two(problem_input: list[str]) -> int:
    elves: set[Position] = set()
    for y, line in enumerate(problem_input):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))

    round_index = 0
    is_done = False
    while not is_done:
        next_elves = run_round(elves, round_index)
        if next_elves is None:
            is_done = True
            break
        elves = next_elves
        round_index += 1

    return round_index + 1


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
