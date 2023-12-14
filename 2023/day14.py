from utils import get_and_cache_input

Position = tuple[int, int]


def slide_rocks_north(
    num_rows: int, num_cols: int, cube_rocks: set[Position], round_rocks: set[Position]
) -> set[Position]:
    moved_round_rocks: set[Position] = set()

    for col in range(num_cols):
        num_rocks = 0
        for row in range(num_rows - 1, -1, -1):
            if (row, col) in cube_rocks:
                for r in range(num_rocks):
                    moved_round_rocks.add((row + r + 1, col))
                num_rocks = 0
                continue
            if (row, col) in round_rocks:
                num_rocks += 1

            if row == 0:
                for r in range(num_rocks):
                    moved_round_rocks.add((row + r, col))

    return moved_round_rocks


def slide_rocks_east(
    num_rows: int, num_cols: int, cube_rocks: set[Position], round_rocks: set[Position]
) -> set[Position]:
    moved_round_rocks: set[Position] = set()

    for row in range(num_rows):
        num_rocks = 0
        for col in range(num_cols):
            if (row, col) in cube_rocks:
                for c in range(num_rocks):
                    moved_round_rocks.add((row, col - c - 1))
                num_rocks = 0
                continue
            if (row, col) in round_rocks:
                num_rocks += 1

            if col == num_cols - 1:
                for c in range(num_rocks):
                    moved_round_rocks.add((row, col - c))

    return moved_round_rocks


def slide_rocks_south(
    num_rows: int, num_cols: int, cube_rocks: set[Position], round_rocks: set[Position]
) -> set[Position]:
    moved_round_rocks: set[Position] = set()

    for col in range(num_cols):
        num_rocks = 0
        for row in range(num_rows):
            if (row, col) in cube_rocks:
                for r in range(num_rocks):
                    moved_round_rocks.add((row - r - 1, col))
                num_rocks = 0
                continue
            if (row, col) in round_rocks:
                num_rocks += 1

            if row == num_rows - 1:
                for r in range(num_rocks):
                    moved_round_rocks.add((row - r, col))

    return moved_round_rocks


def slide_rocks_west(
    num_rows: int, num_cols: int, cube_rocks: set[Position], round_rocks: set[Position]
) -> set[Position]:
    moved_round_rocks: set[Position] = set()

    for row in range(num_rows):
        num_rocks = 0
        for col in range(num_cols - 1, -1, -1):
            if (row, col) in cube_rocks:
                for c in range(num_rocks):
                    moved_round_rocks.add((row, col + c + 1))
                num_rocks = 0
                continue
            if (row, col) in round_rocks:
                num_rocks += 1

            if col == 0:
                for c in range(num_rocks):
                    moved_round_rocks.add((row, col + c))

    return moved_round_rocks


def compute_load_on_north(distance_to_south_edge: int, round_rocks: set[Position]) -> int:
    return sum(distance_to_south_edge - row for row, _ in round_rocks)


def part_one(problem_input: list[str]) -> int:
    round_rocks: set[Position] = set()
    cube_rocks: set[Position] = set()
    for row, line in enumerate(problem_input):
        for col, c in enumerate(line):
            if c == "#":
                cube_rocks.add((row, col))
            elif c == "O":
                round_rocks.add((row, col))

    distance_to_south_edge = len(problem_input)
    return sum(
        distance_to_south_edge - row
        for row, _ in slide_rocks_north(
            len(problem_input), len(problem_input[0]), cube_rocks, round_rocks
        )
    )


def part_two(problem_input: list[str]) -> int:
    round_rocks: set[Position] = set()
    cube_rocks: set[Position] = set()
    for row, line in enumerate(problem_input):
        for col, c in enumerate(line):
            if c == "#":
                cube_rocks.add((row, col))
            elif c == "O":
                round_rocks.add((row, col))

    num_rows, num_cols = len(problem_input), len(problem_input[0])

    settled_rocks: set[Position] = round_rocks.copy()
    for _ in range(1_000_000_000):
        settled_rocks = slide_rocks_north(num_rows, num_cols, cube_rocks, settled_rocks)
        settled_rocks = slide_rocks_west(num_rows, num_cols, cube_rocks, settled_rocks)
        settled_rocks = slide_rocks_south(num_rows, num_cols, cube_rocks, settled_rocks)
        settled_rocks = slide_rocks_east(num_rows, num_cols, cube_rocks, settled_rocks)

    distance_to_south_edge = len(problem_input)
    return sum(distance_to_south_edge - row for row, _ in settled_rocks)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
