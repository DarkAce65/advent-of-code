from utils import get_and_cache_input


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
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
