from utils import get_and_cache_input

PRIORITIES = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def score(char: str) -> int:
    return PRIORITIES.index(char) + 1


def part_one(problem_input: list[str]) -> int:
    sum_of_scores = 0
    for rucksack in problem_input:
        mid = int(len(rucksack) / 2)
        first = rucksack[:mid]
        second = rucksack[mid:]
        overlap = list(set(first).intersection(set(second)))[0]
        sum_of_scores += score(overlap)

    return sum_of_scores


def part_two(problem_input: list[str]) -> int:
    sum_of_scores = 0
    for i in range(0, len(problem_input), 3):
        first, second, third = problem_input[i : i + 3]
        overlap = list(set(first).intersection(set(second)).intersection(set(third)))[0]
        sum_of_scores += score(overlap)

    return sum_of_scores


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
