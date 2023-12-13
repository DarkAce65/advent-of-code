from typing import Literal

from utils import get_and_cache_input


def get_mirror_location(
    grid: list[str],
) -> tuple[Literal["horizontal"] | Literal["vertical"], int]:
    for horizontal in range(1, len(grid)):
        if all(
            grid[horizontal - i - 1] == grid[horizontal + i]
            for i in range(0, min(horizontal, len(grid) - horizontal))
        ):
            return ("horizontal", horizontal)

    for vertical in range(1, len(grid[0])):
        if all(
            all(
                grid[row][vertical - i - 1] == grid[row][vertical + i]
                for i in range(0, min(vertical, len(grid[row]) - vertical))
            )
            for row in range(len(grid))
        ):
            return ("vertical", vertical)

    raise ValueError(f"Couldn't find a horizontal or vertical mirror in grid {grid}")


def part_one(grids: list[list[str]]) -> int:
    result = 0
    for grid in grids:
        direction, index = get_mirror_location(grid)

        if direction == "horizontal":
            result += index * 100
        elif direction == "vertical":
            result += index

    return result


def get_mirror_location_with_smudge(
    grid: list[str],
) -> tuple[Literal["horizontal"] | Literal["vertical"], int]:
    for horizontal in range(1, len(grid)):
        differences = 0
        for i in range(0, min(horizontal, len(grid) - horizontal)):
            if grid[horizontal - i - 1] != grid[horizontal + i]:
                differences += sum(
                    a != b
                    for (a, b) in zip(grid[horizontal - i - 1], grid[horizontal + i])
                )
                if differences > 1:
                    break

        if differences == 1:
            return ("horizontal", horizontal)

    for vertical in range(1, len(grid[0])):
        differences = 0
        for row in range(len(grid)):
            should_break = False
            for i in range(0, min(vertical, len(grid[row]) - vertical)):
                if grid[row][vertical - i - 1] != grid[row][vertical + i]:
                    differences += 1
                    if differences > 1:
                        should_break = True
                        break
            if should_break:
                break
        if differences == 1:
            return ("vertical", vertical)

    raise ValueError(f"Couldn't find a horizontal or vertical mirror in grid {grid}")


def part_two(grids: list[list[str]]) -> int:
    result = 0
    for grid in grids:
        direction, index = get_mirror_location_with_smudge(grid)

        if direction == "horizontal":
            result += index * 100
        elif direction == "vertical":
            result += index

    return result


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    grids: list[list[str]] = []
    grid: list[str] = []
    for line in problem_input:
        if len(line) == 0:
            grids.append(grid)
            grid = []
        else:
            grid.append(line)
    if len(grid) > 0:
        grids.append(grid)

    print("Part One: ", part_one(grids))
    print("Part Two: ", part_two(grids))
