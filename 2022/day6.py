from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    unique = []
    for i, c in enumerate(problem_input[0]):
        unique.append(c)
        if len(unique) == 4:
            if len(set(unique)) == 4:
                return i + 1
            unique.pop(0)

    return 0


def part_two(problem_input: list[str]) -> int:
    unique = []
    for i, c in enumerate(problem_input[0]):
        unique.append(c)
        if len(unique) == 14:
            if len(set(unique)) == 14:
                return i + 1
            unique.pop(0)

    return 0


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
