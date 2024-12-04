from utils import get_and_cache_input


def is_report_safe(report: list[int]) -> bool:
    previous = report[0]
    increasing = previous < report[1]
    for level in report[1:]:
        diff = abs(previous - level)
        if (
            diff < 1
            or diff > 3
            or (increasing and previous > level)
            or (not increasing and previous < level)
        ):
            return False
        previous = level
    return True


def is_report_safe_ignoring_bad_reading(report: list[int]) -> bool:
    if is_report_safe(report):
        return True

    for index in range(len(report)):
        r = report.copy()
        del r[index]
        if is_report_safe(r):
            return True

    return False


def part_one(problem_input: list[str]) -> int:
    return sum(
        1 if is_report_safe([int(level) for level in report.split()]) else 0
        for report in problem_input
    )


def part_two(problem_input: list[str]) -> int:
    return sum(
        (
            1
            if is_report_safe_ignoring_bad_reading(
                [int(level) for level in report.split()]
            )
            else 0
        )
        for report in problem_input
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
