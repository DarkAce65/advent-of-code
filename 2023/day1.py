import re
from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    sum = 0

    for line in problem_input:
        x, y = None, None
        for c in line:
            if c.isnumeric():
                if x is None:
                    x = int(c)
                    y = int(c)
                else:
                    y = int(c)
        if x is None or y is None:
            raise ValueError(line)
        sum += x * 10 + y

    return sum


map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_two(problem_input: list[str]) -> int:
    sum = 0

    for line in problem_input:
        replaced_line = ""
        buffer = ""
        for c in line:
            if c.isalpha():
                buffer += c
            else:
                replaced_line += buffer
                replaced_line += c
                buffer = c
            if buffer:
                for key in map.keys():
                    if buffer.endswith(key):
                        replaced_line += buffer.removesuffix(key) + str(map[key])
                        buffer = c
        replaced_line += buffer

        x, y = None, None
        for c in replaced_line:
            if c.isnumeric():
                if x is None:
                    x = int(c)
                    y = int(c)
                else:
                    y = int(c)
        if x is None or y is None:
            raise ValueError(replaced_line)
        sum += x * 10 + y

    return sum


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
