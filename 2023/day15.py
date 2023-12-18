from collections import OrderedDict, defaultdict

from utils import get_and_cache_input


def hash(string: str) -> int:
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256

    return value


def part_one(problem_input: list[str]) -> int:
    return sum(hash(step) for step in problem_input[0].split(","))


def part_two(problem_input: list[str]) -> int:
    lenses: dict[int, OrderedDict[str, int]] = defaultdict(OrderedDict)
    for step in problem_input[0].split(","):
        if "=" in step:
            label, focal_length = step.split("=")
            lenses[hash(label)][label] = int(focal_length)
        elif "-" in step:
            label = step.removesuffix("-")
            key = hash(label)
            if key in lenses and label in lenses[key]:
                lenses[key].pop(label)

    return sum(
        sum(
            (box + 1) * (lens_index + 1) * focal_length
            for lens_index, focal_length in enumerate(lenses[box].values())
        )
        for box in lenses
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
