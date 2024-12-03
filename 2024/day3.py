from utils import get_and_cache_input

import re


def compute(input: str) -> int:
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input)
    return sum(int(x) * int(y) for x, y in matches)


def part_one(problem_input: list[str]) -> int:
    original_input = "".join(problem_input)
    return compute(original_input)


def part_two(problem_input: list[str]) -> int:
    original_input = "".join(problem_input)

    enabled = True
    input = ""
    for index, c in enumerate(original_input):
        if (
            enabled
            and original_input[index : min(index + 7, len(original_input) - 1)]
            == "don't()"
        ):
            enabled = False
        elif not enabled and original_input[max(0, index - 4) : index] == "do()":
            input += "x"
            enabled = True

        if enabled:
            input += c

    return compute(input)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
