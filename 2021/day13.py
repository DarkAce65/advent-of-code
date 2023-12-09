from typing import Tuple

from utils import get_and_cache_input


class TransparentPaper:
    grid: list[list[bool]]

    def __init__(self, dots: list[Tuple[int, int]]) -> None:
        (max_x, max_y) = (0, 0)
        for dot in dots:
            (x, y) = dot
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        self.grid = []
        for _ in range(max_y + 1):
            self.grid.append([False] * (max_x + 1))

        for dot in dots:
            (x, y) = dot
            self.grid[y][x] = True

    def fold(self, axis: str, value: int) -> None:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x]:
                    if axis == "X" and x > value:
                        self.grid[y][value - (x - value)] = True
                    elif axis == "Y" and y > value:
                        self.grid[value - (y - value)][x] = True

        if axis == "X":
            for y in range(len(self.grid)):
                self.grid[y] = self.grid[y][:value]
        else:
            self.grid = self.grid[:value]

    def get_num_dots(self) -> int:
        num_dots = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x]:
                    num_dots += 1

        return num_dots

    def __repr__(self) -> str:
        s = ""

        for row in self.grid:
            for cell in row:
                if cell:
                    s += "#"
                else:
                    s += "."
            s += "\n"

        return s


def part_one(paper: TransparentPaper, instructions: list[str]) -> int:
    [axis, value] = instructions[0].lstrip("fold along ").split("=")
    paper.fold(axis.upper(), int(value))

    return paper.get_num_dots()


def part_two(paper: TransparentPaper, instructions: list[str]) -> str:
    for instruction in instructions:
        [axis, value] = instruction.lstrip("fold along ").split("=")
        paper.fold(axis.upper(), int(value))

    return str(paper)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    dots = []
    instructions = []

    for line in problem_input:
        if not line:
            continue

        if line.startswith("fold along"):
            instructions.append(line)
        else:
            [x, y] = map(int, line.split(","))
            dots.append((x, y))

    paper = TransparentPaper(dots)

    print("Part One: ", part_one(paper, instructions))
    print("Part Two:")
    print(part_two(paper, instructions))
