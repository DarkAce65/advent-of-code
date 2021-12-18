import json
import math
import re
from pathlib import Path


def reduce_number(snailfish_number: str) -> str:
    index = 0

    depth = 0
    while index < len(snailfish_number):
        c = snailfish_number[index]
        if c == "[":
            depth += 1
            if depth > 4:
                exploding_pair_match = next(
                    re.finditer(r"\[\d+,\d+\]", snailfish_number[index:])
                )
                open_index = index + exploding_pair_match.start(0)
                close_index = index + exploding_pair_match.end(0)
                exploding_pair = json.loads(exploding_pair_match.group(0))
                before_str = snailfish_number[:open_index]
                after_str = snailfish_number[close_index:]

                try:
                    match = next(re.finditer(r"(\d+)[^\d]*$", before_str))
                    left_number = int(match.group(1))
                    left_number += exploding_pair[0]
                    before_str = (
                        before_str[: match.start(1)]
                        + str(left_number)
                        + before_str[match.end(1) :]
                    )
                except StopIteration:
                    pass

                try:
                    match = next(re.finditer(r"^[^\d]*(\d+)", after_str))
                    right_number = int(match.group(1))
                    right_number += exploding_pair[1]
                    after_str = (
                        after_str[: match.start(1)]
                        + str(right_number)
                        + after_str[match.end(1) :]
                    )
                except StopIteration:
                    pass

                return reduce_number(before_str + "0" + after_str)
        elif c == "]":
            depth -= 1

        index += 1

    split_match = re.search(r"\d{2,}", snailfish_number)
    if split_match is not None:
        return reduce_number(
            snailfish_number[: split_match.start(0)]
            + "["
            + str(math.floor(int(split_match.group(0)) / 2))
            + ","
            + str(math.ceil(int(split_match.group(0)) / 2))
            + "]"
            + snailfish_number[split_match.end(0) :]
        )

    return snailfish_number


def add_numbers(snailfish_number1: str, snailfish_number2: str) -> str:
    return reduce_number("[" + snailfish_number1 + "," + snailfish_number2 + "]")


def part_one(snailfish_numbers: list[str]) -> int:
    snailfish_number = snailfish_numbers[0]
    for s in snailfish_numbers[1:]:
        print("  " + snailfish_number, s, sep="\n+ ")
        snailfish_number = add_numbers(snailfish_number, s)
        print("= " + snailfish_number)

    return 0


def part_two(snailfish_numbers: list[str]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
