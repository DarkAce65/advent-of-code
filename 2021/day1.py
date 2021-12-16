from pathlib import Path


def part_one(depths: list[int]) -> int:
    num_increases = 0
    prev_depth = depths[0]
    for depth in depths[1:]:
        if depth > prev_depth:
            num_increases += 1
        prev_depth = depth

    return num_increases


def part_two(depths: list[int]) -> int:
    num_increases = 0
    for i in range(3, len(depths)):
        if sum(depths[i - 2 : i + 1]) > sum(depths[i - 3 : i]):
            num_increases += 1

    return num_increases


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [int(line.rstrip()) for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
