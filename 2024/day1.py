from collections import defaultdict

from utils import get_and_cache_input


def part_one(problem_input: list[str]) -> int:
    list1: list[int] = []
    list2: list[int] = []
    for line in problem_input:
        value1, value2 = line.split()
        list1.append(int(value1))
        list2.append(int(value2))

    list1.sort()
    list2.sort()
    return sum(abs(list2[i] - list1[i]) for i in range(len(problem_input)))


def part_two(problem_input: list[str]) -> int:
    base_numbers: dict[int, int] = defaultdict(lambda: 0)
    occurrences: dict[int, int] = defaultdict(lambda: 0)
    for line in problem_input:
        value1, value2 = line.split()
        base_numbers[int(value1)] += 1
        occurrences[int(value2)] += 1

    return sum(
        base_number * times * occurrences.get(base_number, 0)
        for base_number, times in base_numbers.items()
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
