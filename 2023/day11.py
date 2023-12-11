from utils import get_and_cache_input


def compute_galaxy_distances(problem_input: list[str], expansion_multiplier: int) -> int:
    galaxies: list[tuple[int, int]] = []
    empty_rows = set(range(len(problem_input)))
    empty_columns = set(range(len(problem_input[0])))
    for row, _ in enumerate(problem_input):
        for col, pixel in enumerate(problem_input[row]):
            if pixel == "#":
                galaxies.append((row, col))

                if row in empty_rows:
                    empty_rows.remove(row)
                if col in empty_columns:
                    empty_columns.remove(col)

    result = 0
    for index, (row, col) in enumerate(galaxies):
        for other_row, other_col in galaxies[index:]:
            result += sum(
                (expansion_multiplier if r in empty_rows else 1)
                for r in range(min(row, other_row), max(row, other_row))
            ) + sum(
                (expansion_multiplier if c in empty_columns else 1)
                for c in range(min(col, other_col), max(col, other_col))
            )

    return result


def part_one(problem_input: list[str]) -> int:
    return compute_galaxy_distances(problem_input, 2)


def part_two(problem_input: list[str]) -> int:
    return compute_galaxy_distances(problem_input, 1_000_000)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
