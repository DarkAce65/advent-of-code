from pathlib import Path

Instruction = tuple[bool, tuple[int, int], tuple[int, int], tuple[int, int]]


def parse_instructions(problem_input: list[str]) -> list[Instruction]:
    instructions = []
    for instruction in problem_input:
        [state, bounds] = instruction.split()
        [x_bounds, y_bounds, z_bounds] = bounds.split(",")
        [x_low, x_high] = list(map(int, x_bounds[2:].split("..")))
        [y_low, y_high] = list(map(int, y_bounds[2:].split("..")))
        [z_low, z_high] = list(map(int, z_bounds[2:].split("..")))
        instructions.append(
            (
                True if state == "on" else False,
                (x_low, x_high),
                (y_low, y_high),
                (z_low, z_high),
            )
        )

    return instructions


def part_one(instructions: list[Instruction]) -> int:
    enabled_cubes: set[tuple[int, int, int]] = set()
    for (should_enable, x_bounds, y_bounds, z_bounds) in instructions:
        for x in range(x_bounds[0], x_bounds[1] + 1):
            if x < -50 or 50 < x:
                continue
            for y in range(y_bounds[0], y_bounds[1] + 1):
                if y < -50 or 50 < y:
                    continue
                for z in range(z_bounds[0], z_bounds[1] + 1):
                    if z < -50 or 50 < z:
                        continue
                    if should_enable:
                        enabled_cubes.add((x, y, z))
                    else:
                        if (x, y, z) in enabled_cubes:
                            enabled_cubes.remove((x, y, z))

    return len(enabled_cubes)


def part_two(instructions: list[Instruction]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    instructions = parse_instructions(problem_input)

    print("Part One: ", part_one(instructions))
    print("Part Two: ", part_two(instructions))
