from pathlib import Path


def parse_starting_positions(problem_input: list[str]) -> list[int]:
    starting_positions = []
    for line in problem_input:
        [_, starting_position] = line.split(":")
        starting_positions.append(int(starting_position.strip()))

    return starting_positions


def part_one(starting_positions: list[int]) -> int:
    positions = starting_positions.copy()
    scores = []
    for _ in positions:
        scores.append(0)

    turn = 0
    roll = 1 + 2 + 3
    num_rolls = 3
    while True:
        positions[turn] = (positions[turn] - 1 + roll) % 10 + 1
        scores[turn] += positions[turn]
        if scores[turn] >= 1000:
            break
        turn = (turn + 1) % len(positions)
        roll += 9
        num_rolls += 3

    return min(scores) * num_rolls


def part_two(starting_positions: list[int]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    starting_positions = parse_starting_positions(problem_input)

    print("Part One: ", part_one(starting_positions))
    print("Part Two: ", part_two(starting_positions))
