import re
from collections import defaultdict
from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    points = 0
    for line in problem_input:
        _, numbers_str = line.split(":", maxsplit=2)
        winning_numbers_str, numbers = numbers_str.split("|")

        winning_numbers = set(winning_numbers_str.strip().split())
        wins = 0
        for number in numbers.strip().split():
            if number in winning_numbers:
                wins += 1
        if wins > 0:
            points += 2 ** (wins - 1)

    return points


def part_two(problem_input: list[str]) -> int:
    card_counts: dict[int, int] = defaultdict(int)
    for line in problem_input:
        card_str, numbers_str = line.split(":", maxsplit=2)
        card_number = int(re.match(r"Card\s+(\d+)", card_str).group(1))
        winning_numbers_str, numbers = numbers_str.split("|")

        winning_numbers = set(winning_numbers_str.strip().split())
        wins = 0
        for number in numbers.strip().split():
            if number in winning_numbers:
                wins += 1

        card_counts[card_number] += 1
        for w in range(wins):
            card_counts[card_number + w + 1] += card_counts[card_number]

    return sum(card_counts.values())


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
