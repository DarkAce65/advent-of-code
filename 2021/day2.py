from pathlib import Path


def part_one(instructions: list[str]) -> int:
    (pos, depth) = (0, 0)

    for instruction in instructions:
        (command, value_str) = instruction.split(" ")
        value = int(value_str)
        if command == "forward":
            pos += value
        elif command == "down":
            depth += value
        elif command == "up":
            depth -= value

    return pos * depth


def part_two(instructions: list[str]):
    (pos, depth, aim) = (0, 0, 0)

    for instruction in instructions:
        (command, value_str) = instruction.split(" ")
        value = int(value_str)
        if command == "forward":
            pos += value
            depth += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value

    return pos * depth


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
