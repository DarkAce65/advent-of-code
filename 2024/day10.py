from typing import NamedTuple
from utils import get_and_cache_input


class Position(NamedTuple):
    row: int
    col: int


def get_neighbors(grid: list[list[int]], position: Position) -> set[Position]:
    row, col = position
    height = grid[row][col]

    neighbors: set[Position] = set()
    if row - 1 >= 0 and grid[row - 1][col] == height + 1:
        neighbors.add(Position(row - 1, col))
    if row + 1 < len(grid) and grid[row + 1][col] == height + 1:
        neighbors.add(Position(row + 1, col))
    if col - 1 >= 0 and grid[row][col - 1] == height + 1:
        neighbors.add(Position(row, col - 1))
    if col + 1 < len(grid[row]) and grid[row][col + 1] == height + 1:
        neighbors.add(Position(row, col + 1))

    return neighbors


def find_reachable_peaks(
    reachable_peaks: list[list[set[Position] | None]],
    grid: list[list[int]],
    position: Position,
) -> set[Position] | None:
    row, col = position

    if reachable_peaks[row][col] is None:
        if grid[row][col] == 9:
            reachable_peaks[row][col] = set([position])
        else:
            all_peaks: set[Position] = set()
            for neighbor in get_neighbors(grid, position):
                peaks = find_reachable_peaks(reachable_peaks, grid, neighbor)
                if peaks is not None:
                    for peak in peaks:
                        all_peaks.add(peak)
            reachable_peaks[row][col] = all_peaks

    return reachable_peaks[row][col]


def count_paths_to_top(
    num_paths_grid: list[list[int | None]],
    grid: list[list[int]],
    position: Position,
) -> int:
    row, col = position

    if num_paths_grid[row][col] is None:
        if grid[row][col] == 9:
            num_paths_grid[row][col] = 1
        else:
            paths = 0
            for neighbor in get_neighbors(grid, position):
                paths += count_paths_to_top(num_paths_grid, grid, neighbor)
            num_paths_grid[row][col] = paths

    num_paths = num_paths_grid[row][col]
    assert num_paths is not None
    return num_paths


def parse_map(
    problem_input: list[str],
) -> tuple[list[list[set[Position] | None]], list[list[int | None]], set[Position]]:
    grid: list[list[int]] = []
    reachable_peaks: list[list[set[Position] | None]] = []
    num_paths_grid: list[list[int | None]] = []
    trailheads: set[Position] = set()
    for r, row in enumerate(problem_input):
        grid.append([])
        reachable_peaks.append([])
        num_paths_grid.append([])
        for c, cell in enumerate(row):
            height = int(cell)
            grid[r].append(height)
            reachable_peaks[r].append(None)
            num_paths_grid[r].append(None)
            if height == 0:
                trailheads.add(Position(r, c))

    for trailhead in trailheads:
        find_reachable_peaks(reachable_peaks, grid, trailhead)
        count_paths_to_top(num_paths_grid, grid, trailhead)

    return (reachable_peaks, num_paths_grid, trailheads)


def part_one(problem_input: list[str]) -> int:
    reachable_peaks, _, trailheads = parse_map(problem_input)

    total_score = 0
    for row, col in trailheads:
        peaks = reachable_peaks[row][col]
        if peaks is not None:
            total_score += len(peaks)

    return total_score


def part_two(problem_input: list[str]) -> int:
    _, num_paths_grid, trailheads = parse_map(problem_input)

    total_rating = 0
    for row, col in trailheads:
        paths = num_paths_grid[row][col]
        if paths is not None:
            total_rating += paths

    return total_rating


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
