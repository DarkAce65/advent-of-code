from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    result = 0
    for line in problem_input:
        counts = [int(x) for x in line.split()]
        diffs = [counts]
        while not all(x == 0 for x in diffs[-1]):
            diff = []
            for index in range(len(diffs[-1]) - 1):
                diff.append(diffs[-1][index + 1] - diffs[-1][index])
            diffs.append(diff)

        for index in range(len(diffs) - 2, -1, -1):
            diffs[index].append(diffs[index][-1] + diffs[index + 1][-1])

        result += diffs[0][-1]
    return result


def part_two(problem_input: list[str]) -> int:
    result = 0
    for line in problem_input:
        counts = [int(x) for x in line.split()]
        diffs = [counts]
        while not all(x == 0 for x in diffs[-1]):
            diff = []
            for index in range(len(diffs[-1]) - 1):
                diff.append(diffs[-1][index + 1] - diffs[-1][index])
            diffs.append(diff)

        for index in range(len(diffs) - 2, -1, -1):
            diffs[index].insert(0, diffs[index][0] - diffs[index + 1][0])

        result += diffs[0][0]
    return result


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
