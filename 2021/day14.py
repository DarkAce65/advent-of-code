from collections import Counter
from pathlib import Path
from typing import Optional, Tuple


def polymerize(polymer: str, insertion_rules: dict[str, str]) -> str:
    next_polymer = polymer
    num_inserted_elements = 0
    for index in range(len(polymer) - 1):
        current_pair = polymer[index : index + 2]
        if current_pair in insertion_rules:
            next_polymer = (
                next_polymer[: num_inserted_elements + index + 1]
                + insertion_rules[current_pair]
                + next_polymer[num_inserted_elements + index + 1 :]
            )
            num_inserted_elements += 1

    return next_polymer


def part_one(starting_template: str, insertion_rules: dict[str, str]) -> int:
    polymer = starting_template
    for _ in range(10):
        polymer = polymerize(polymer, insertion_rules)

    element_counts = Counter(polymer)
    most_common = max(element_counts, key=element_counts.__getitem__)
    least_common = min(element_counts, key=element_counts.__getitem__)

    return element_counts[most_common] - element_counts[least_common]


cache: dict[str, Counter[str]] = {}


def get_expansion_counts(
    pair: str, insertion_rules: dict[str, str], steps: int
) -> Optional[Counter[str]]:
    if steps <= 0 or pair not in insertion_rules:
        return None

    cache_key = pair + str(steps)
    if cache_key in cache:
        return cache[cache_key]

    inserted_element = insertion_rules[pair]
    element_counts = Counter(insertion_rules[pair])
    left_pair_counts = get_expansion_counts(
        pair[0] + inserted_element, insertion_rules, steps - 1
    )
    if left_pair_counts is not None:
        element_counts += left_pair_counts

    right_pair_counts = get_expansion_counts(
        inserted_element + pair[1], insertion_rules, steps - 1
    )
    if right_pair_counts is not None:
        element_counts += right_pair_counts

    cache[cache_key] = element_counts
    return element_counts


def part_two(starting_template: str, insertion_rules: dict[str, str]) -> int:
    element_counts: Counter[str] = Counter(starting_template)
    polymer = starting_template

    for index in range(len(polymer) - 1):
        current_pair = polymer[index : index + 2]
        counts = get_expansion_counts(current_pair, insertion_rules, 40)
        if counts is not None:
            element_counts += counts

    most_common = max(element_counts, key=element_counts.__getitem__)
    least_common = min(element_counts, key=element_counts.__getitem__)

    return element_counts[most_common] - element_counts[least_common]


def parse_rule(rule: str) -> Tuple[str, str]:
    [pattern, insertion] = rule.split(" -> ", maxsplit=1)
    return (pattern, insertion)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    starting_template = problem_input[0]
    insertion_rules: dict[str, str] = {
        pattern: insertion
        for (pattern, insertion) in map(parse_rule, filter(None, problem_input[1:]))
    }

    print("Part One: ", part_one(starting_template, insertion_rules))
    print("Part Two: ", part_two(starting_template, insertion_rules))
