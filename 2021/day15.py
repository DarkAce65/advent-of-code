import copy
import heapq
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple


@dataclass(order=True)
class PrioritizedCell:
    location: Tuple[int, int] = field(compare=False)
    priority: int


def djikstra(grid: list[list[int]]) -> int:
    open_cells: list[PrioritizedCell] = []
    cost_so_far: dict[Tuple[int, int], int] = {}

    end = (len(grid) - 1, len(grid[0]) - 1)

    cost_so_far[(0, 0)] = 0
    heapq.heappush(
        open_cells, PrioritizedCell(location=(0, 0), priority=cost_so_far[(0, 0)])
    )

    while len(open_cells) > 0:
        current_cell = heapq.heappop(open_cells)

        if current_cell.location == end:
            break

        (row, col) = current_cell.location
        neighbors: list[Tuple[int, int]] = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < len(grid) - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < len(grid[row]) - 1:
            neighbors.append((row, col + 1))
        for neighbor in neighbors:
            cost = cost_so_far[(row, col)] + grid[neighbor[0]][neighbor[1]]
            if neighbor not in cost_so_far or cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = cost
                heapq.heappush(
                    open_cells, PrioritizedCell(location=neighbor, priority=cost)
                )

    return cost_so_far[end]


def part_one(grid: list[list[int]]) -> int:
    return djikstra(grid)


def part_two(grid: list[list[int]]) -> int:
    expanded_grid: list[list[int]] = []

    for row in range(len(grid)):
        expanded_row = grid[row].copy()
        for i in range(4):
            expanded_row += list(map(lambda cell: (cell + i) % 9 + 1, grid[row]))
        expanded_grid.append(expanded_row)

    for i in range(4):
        for row in range(len(grid)):
            expanded_row = list(map(lambda cell: (cell + i) % 9 + 1, expanded_grid[row]))
            expanded_grid.append(expanded_row)

    return djikstra(expanded_grid)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    grid = [list(map(int, line)) for line in problem_input]

    print("Part One: ", part_one(grid))
    print("Part Two: ", part_two(grid))
