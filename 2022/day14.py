import math
from pathlib import Path

sand_start_point = (500, 0)


class SandSimulation:
    map: set[tuple[int, int]]

    def __init__(self) -> None:
        self.map = set()

    def place_rock(self, rock_path: list[tuple[int, int]]):
        for i in range(len(rock_path) - 1):
            x_current, y_current = rock_path[i]
            x_end, y_end = rock_path[i + 1]
            if x_current == x_end:
                while y_current != y_end:
                    self.map.add((x_current, y_current))
                    y_current += int(math.copysign(1, y_end - y_current))
                self.map.add((x_current, y_current))
            elif y_current == y_end:
                while x_current != x_end:
                    self.map.add((x_current, y_current))
                    x_current += int(math.copysign(1, x_end - x_current))
                self.map.add((x_current, y_current))

    def compute_bounds(self) -> tuple[tuple[int, int], tuple[int, int]]:
        x_bounds = (sand_start_point[0], sand_start_point[0])
        y_bounds = (sand_start_point[1], sand_start_point[1])
        for x, y in self.map:
            if x < x_bounds[0]:
                x_bounds = (x, x_bounds[1])
            elif x_bounds[1] < x:
                x_bounds = (x_bounds[0], x)
            if y < y_bounds[0]:
                y_bounds = (y, y_bounds[1])
            elif y_bounds[1] < y:
                y_bounds = (y_bounds[0], y)

        return (x_bounds, y_bounds)

    def build_grid(self) -> tuple[list[list[str]], tuple[int, int]]:
        (x_min, x_max), (y_min, y_max) = self.compute_bounds()

        grid: list[list[str]] = []
        drop_point = (0, 0)
        for j, y in enumerate(range(y_min, y_max + 1)):
            grid.append([])
            for i, x in enumerate(range(x_min, x_max + 1)):
                cell = "."
                if (x, y) == sand_start_point:
                    cell = "+"
                    drop_point = (i, j)
                elif (x, y) in self.map:
                    cell = "#"

                grid[y].append(cell)

        return (grid, drop_point)


def get_in_grid(grid: list[list[str]], position: tuple[int, int]) -> str:
    x, y = position
    return grid[y][x]


def simulate_sand_drop(
    grid: list[list[str]], drop_point: tuple[int, int]
) -> list[list[str]]:
    current_grain = drop_point
    while (
        1 <= current_grain[0]
        and current_grain[0] < len(grid[0]) - 1
        and 0 <= current_grain[1]
        and current_grain[1] < len(grid) - 1
        and get_in_grid(grid, (current_grain[0], current_grain[1])) != "o"
    ):
        if get_in_grid(grid, (current_grain[0], current_grain[1] + 1)) == ".":
            current_grain = (current_grain[0], current_grain[1] + 1)
        elif get_in_grid(grid, (current_grain[0] - 1, current_grain[1] + 1)) == ".":
            current_grain = (current_grain[0] - 1, current_grain[1] + 1)
        elif get_in_grid(grid, (current_grain[0] + 1, current_grain[1] + 1)) == ".":
            current_grain = (current_grain[0] + 1, current_grain[1] + 1)
        else:
            grid[current_grain[1]][current_grain[0]] = "o"
            current_grain = drop_point

    return grid


def part_one(problem_input: list[str]) -> int:
    sim = SandSimulation()

    for line in problem_input:
        rock_path = []
        for coordinates in line.split("->"):
            x, y = coordinates.strip().split(",")
            rock_path.append((int(x), int(y)))
        sim.place_rock(rock_path)

    grid, drop_point = sim.build_grid()
    simulate_sand_drop(grid, drop_point)

    return sum(sum(1 for c in row if c == "o") for row in grid)


def part_two(problem_input: list[str]) -> int:
    sim = SandSimulation()

    for line in problem_input:
        rock_path = []
        for coordinates in line.split("->"):
            x, y = coordinates.strip().split(",")
            rock_path.append((int(x), int(y)))
        sim.place_rock(rock_path)

    _, (_, y_max) = sim.compute_bounds()
    new_y_max = y_max + 2
    sim.place_rock(
        [
            (sand_start_point[0] - new_y_max, new_y_max),
            (sand_start_point[0] + new_y_max, new_y_max),
        ]
    )

    grid, drop_point = sim.build_grid()
    simulate_sand_drop(grid, drop_point)

    return sum(sum(1 for c in row if c == "o") for row in grid)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
