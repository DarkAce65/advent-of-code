from utils import get_and_cache_input


def can_solve(target: int, sequence: list[int]) -> bool:
    if len(sequence) == 0 or sequence[0] > target:
        return False
    elif len(sequence) == 1:
        return sequence[0] == target

    return can_solve(target, [sequence[0] + sequence[1]] + sequence[2:]) or can_solve(
        target, [sequence[0] * sequence[1]] + sequence[2:]
    )


def can_solve_with_concat(target: int, sequence: list[int]) -> bool:
    if len(sequence) == 0 or sequence[0] > target:
        return False
    elif len(sequence) == 1:
        return sequence[0] == target

    return (
        can_solve_with_concat(target, [sequence[0] + sequence[1]] + sequence[2:])
        or can_solve_with_concat(target, [sequence[0] * sequence[1]] + sequence[2:])
        or can_solve_with_concat(
            target, [int(str(sequence[0]) + str(sequence[1]))] + sequence[2:]
        )
    )


def part_one(problem_input: list[str]) -> int:
    sum = 0
    for line in problem_input:
        target, sequence = line.split(":")
        if can_solve(int(target), [int(v) for v in sequence.strip().split(" ")]):
            sum += int(target)

    return sum


def part_two(problem_input: list[str]) -> int:
    sum = 0
    for line in problem_input:
        target, sequence = line.split(":")
        if can_solve_with_concat(
            int(target), [int(v) for v in sequence.strip().split(" ")]
        ):
            sum += int(target)

    return sum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
