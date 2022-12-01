from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    return 0


def part_two(problem_input: list[str]) -> int:
    return 0


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
