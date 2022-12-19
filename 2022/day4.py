from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    count = 0
    for row in problem_input:
        left, right = row.split(",")
        left_low, left_high = left.split("-")
        right_low, right_high = right.split("-")

        if (int(left_low) <= int(right_low) and int(right_high) <= int(left_high)) or (
            int(right_low) <= int(left_low) and int(left_high) <= int(right_high)
        ):
            count += 1

    return count


def part_two(problem_input: list[str]) -> int:
    count = 0
    for row in problem_input:
        left, right = row.split(",")
        left_low, left_high = left.split("-")
        right_low, right_high = right.split("-")

        if (
            (int(left_low) <= int(right_low) and int(right_low) <= int(left_high))
            or (int(left_low) <= int(right_high) and int(right_high) <= int(left_high))
            or (int(right_low) <= int(left_low) and int(left_low) <= int(right_high))
            or (int(right_low) <= int(left_high) and int(left_high) <= int(right_high))
        ):
            count += 1

    return count


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
