from utils import get_and_cache_input


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
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
