from utils import get_and_cache_input


def part_one(problem_input: list[str]) -> int:
    elves = [0]
    for carry in problem_input:
        if carry == "":
            elves.append(0)
        else:
            elves[-1] += int(carry)

    return max(elves)


def part_two(problem_input: list[str]) -> int:
    elves = [0]
    for carry in problem_input:
        if carry == "":
            elves.append(0)
        else:
            elves[-1] += int(carry)

    return sum(sorted(elves, reverse=True)[:3])


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
