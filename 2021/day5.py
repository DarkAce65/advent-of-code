import sys
from pathlib import Path
from typing import Tuple


def sign(a: int) -> int:
    return (a > 0) - (a < 0)


class GridPlot:
    grid: list[list[int]]

    def __init__(
        self,
        lines: list[Tuple[Tuple[int, int], Tuple[int, int]]],
        max_bounds: Tuple[int, int],
        include_diagonals=True,
    ) -> None:
        (x_bound, y_bound) = max_bounds
        self.grid = []
        for _ in range(x_bound + 1):
            self.grid.append([0] * (y_bound + 1))

        for line in lines:
            (xy1, xy2) = line
            if include_diagonals or (xy1[0] == xy2[0] or xy1[1] == xy2[1]):
                self.place_line(xy1, xy2)

    def place_line(self, xy1: Tuple[int, int], xy2: Tuple[int, int]) -> None:
        (x1, y1) = xy1
        (x2, y2) = xy2

        dx = x2 - x1
        dy = y2 - y1

        def plane_equation(x: int, y: int) -> float:
            return (float(x) - x1) * dy / dx + y1 - float(y)

        x_dir = sign(x2 - x1)
        y_dir = sign(y2 - y1)

        (x, y) = (x1, y1)
        while True:
            self.grid[x][y] += 1

            if x == x2 and y == y2:
                break
            elif x == x2:
                y += y_dir
            elif y == y2:
                x += x_dir
            else:
                diff = abs(plane_equation(x + x_dir, y)) - abs(
                    plane_equation(x, y + y_dir)
                )
                if abs(diff) < sys.float_info.epsilon:
                    x += x_dir
                    y += y_dir
                elif diff < 0:
                    x += x_dir
                else:
                    y += y_dir

    def get_intersection_count(self) -> int:
        intersections = 0
        for column in self.grid:
            for cell in column:
                if cell > 1:
                    intersections += 1

        return intersections

    def __repr__(self) -> str:
        s = ""

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[y][x] == 0:
                    s += "."
                else:
                    s += str(self.grid[y][x])
            s += "\n"

        return s


def part_one(plot: GridPlot) -> int:
    return plot.get_intersection_count()


def part_two(plot: GridPlot) -> int:
    return plot.get_intersection_count()


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    lines: list[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    (max_x, max_y) = (0, 0)
    for line_definition in problem_input:
        [xy1, xy2] = line_definition.split(" -> ", maxsplit=1)
        [x1, y1] = list(map(int, xy1.split(",", maxsplit=1)))
        [x2, y2] = list(map(int, xy2.split(",", maxsplit=1)))

        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)
        lines.append(((x1, y1), (x2, y2)))

    plot_without_diagonals = GridPlot(lines, (max_x, max_y), include_diagonals=False)
    plot_with_diagonals = GridPlot(lines, (max_x, max_y))

    print("Part One: ", part_one(plot_without_diagonals))
    print("Part Two: ", part_two(plot_with_diagonals))
