from collections import defaultdict
from typing import NamedTuple

from utils import get_and_cache_input


class Position(NamedTuple):
    row: int
    col: int


def parse_map(
    problem_input: list[str],
) -> tuple[tuple[int, int], dict[str, set[Position]]]:
    antennas: dict[str, set[Position]] = defaultdict(set)

    for r, row in enumerate(problem_input):
        for c, cell in enumerate(row):
            if cell.isalnum():
                antennas[cell].add(Position(r, c))

    return ((len(problem_input), len(problem_input[0])), antennas)


def find_single_antinodes(
    dimensions: tuple[int, int], antennas: set[Position]
) -> set[Position]:
    height, width = dimensions
    antinodes: set[Position] = set()

    antenna_list = list(antennas)
    for index, antenna1 in enumerate(antenna_list):
        for antenna2 in antenna_list[index + 1 :]:
            antinode1 = Position(
                antenna2.row * 2 - antenna1.row, antenna2.col * 2 - antenna1.col
            )
            antinode2 = Position(
                antenna1.row * 2 - antenna2.row, antenna1.col * 2 - antenna2.col
            )
            if 0 <= antinode1.row < height and 0 <= antinode1.col < width:
                antinodes.add(antinode1)
            if 0 <= antinode2.row < height and 0 <= antinode2.col < width:
                antinodes.add(antinode2)

    return antinodes


def find_antinodes(dimensions: tuple[int, int], antennas: set[Position]) -> set[Position]:
    height, width = dimensions
    antinodes: set[Position] = set()

    antenna_list = list(antennas)
    for index, antenna1 in enumerate(antenna_list):
        for antenna2 in antenna_list[index + 1 :]:
            diff_row = antenna2.row - antenna1.row
            diff_col = antenna2.col - antenna1.col

            antinode = antenna2
            while 0 <= antinode.row < height and 0 <= antinode.col < width:
                antinodes.add(antinode)
                antinode = Position(antinode.row + diff_row, antinode.col + diff_col)
            antinode = Position(antenna2.row - diff_row, antenna2.col - diff_col)
            while 0 <= antinode.row < height and 0 <= antinode.col < width:
                antinodes.add(antinode)
                antinode = Position(antinode.row - diff_row, antinode.col - diff_col)

    return antinodes


def part_one(problem_input: list[str]) -> int:
    dimensions, antenna_positions = parse_map(problem_input)

    antinodes: set[Position] = set()
    for antennas in antenna_positions.values():
        for antinode in find_single_antinodes(dimensions, antennas):
            antinodes.add(antinode)

    return len(antinodes)


def part_two(problem_input: list[str]) -> int:
    dimensions, antenna_positions = parse_map(problem_input)

    antinodes: set[Position] = set()
    for antennas in antenna_positions.values():
        for antinode in find_antinodes(dimensions, antennas):
            antinodes.add(antinode)

    return len(antinodes)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
