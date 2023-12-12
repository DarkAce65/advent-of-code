from functools import lru_cache
from utils import get_and_cache_input


@lru_cache(maxsize=4096)
def compute_possible_ways(remaining_springs: str, groups: str) -> int:
    if len(groups) == 0:
        return 1 if all(c != "#" for c in remaining_springs) else 0

    if "," in (groups):
        item_str, rest = groups.split(",", maxsplit=1)
    else:
        item_str = groups
        rest = ""
    item = int(item_str)
    if len(remaining_springs) < item:
        return 0

    possible_ways = 0
    for index in range(len(remaining_springs) - item + 1):
        if index > 0 and remaining_springs[index - 1] == "#":
            break
        if (
            (index == 0 or remaining_springs[index - 1] != "#")
            and (
                index == len(remaining_springs) - item
                or remaining_springs[index + item] != "#"
            )
            and "." not in remaining_springs[index : index + item]
        ):
            possible_ways += compute_possible_ways(
                remaining_springs[index + item + 1 :], rest
            )
    return possible_ways


def part_one(springs_and_groups: list[tuple[str, str]]) -> int:
    return sum(
        compute_possible_ways(springs, groups) for springs, groups in springs_and_groups
    )


def part_two(springs_and_groups: list[tuple[str, str]]) -> int:
    return sum(
        compute_possible_ways("?".join([springs] * 5), ",".join([groups] * 5))
        for springs, groups in springs_and_groups
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    springs_and_groups: list[tuple[str, str]] = []
    for line in problem_input:
        springs, groups = line.split()
        springs_and_groups.append((springs, groups))

    print("Part One: ", part_one(springs_and_groups))
    print("Part Two: ", part_two(springs_and_groups))
