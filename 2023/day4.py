import re
from collections import defaultdict

from utils import get_and_cache_input


def parse_card(card_line: str) -> tuple[int, set[str], list[str]]:
    card_str, all_numbers_str = card_line.split(":", maxsplit=2)
    card_number_match = re.match(r"Card\s+(\d+)", card_str)
    assert card_number_match is not None
    card_number = int(card_number_match.group(1))
    winning_numbers_str, numbers_str = all_numbers_str.split("|")

    return (
        card_number,
        set(winning_numbers_str.strip().split()),
        numbers_str.strip().split(),
    )


def part_one(problem_input: list[str]) -> int:
    points = 0
    for line in problem_input:
        _, winning_numbers, numbers = parse_card(line)

        wins = sum(1 for number in numbers if number in winning_numbers)
        if wins > 0:
            points += 2 ** (wins - 1)

    return points


def part_two(problem_input: list[str]) -> int:
    card_counts: dict[int, int] = defaultdict(int)
    for line in problem_input:
        card_number, winning_numbers, numbers = parse_card(line)

        card_counts[card_number] += 1
        wins = sum(1 for number in numbers if number in winning_numbers)
        for w in range(wins):
            card_counts[card_number + w + 1] += card_counts[card_number]

    return sum(card_counts.values())


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
