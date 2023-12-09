import math

from utils import get_and_cache_input

part_one_digits = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}
part_two_digits = dict(
    {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    },
    **part_one_digits
)


def part_one(problem_input: list[str]) -> int:
    sum = 0

    for line in problem_input:
        _, first = min(
            ((line.find(key), part_one_digits[key]) for key in part_one_digits),
            key=lambda digit_pair: digit_pair[0] if digit_pair[0] != -1 else math.inf,
        )
        _, last = max(
            ((line.rfind(key), part_one_digits[key]) for key in part_one_digits),
            key=lambda digit_pair: digit_pair[0],
        )
        sum += first * 10 + last

    return sum


def part_two(problem_input: list[str]) -> int:
    sum = 0

    for line in problem_input:
        _, first = min(
            ((line.find(key), part_two_digits[key]) for key in part_two_digits),
            key=lambda digit_pair: digit_pair[0] if digit_pair[0] != -1 else math.inf,
        )
        _, last = max(
            ((line.rfind(key), part_two_digits[key]) for key in part_two_digits),
            key=lambda digit_pair: digit_pair[0],
        )
        sum += first * 10 + last

    return sum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
