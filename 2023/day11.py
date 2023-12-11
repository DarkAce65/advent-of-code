from utils import get_and_cache_input


def part_one(problem_input: list[str]) -> int:
    expanded_image: list[str] = []

    columns_to_expand = set(range(len(problem_input[0])))
    for row, line in enumerate(problem_input):
        row_empty = True
        for col, pixel in enumerate(problem_input[row]):
            if pixel == "#":
                row_empty = False
                if col in columns_to_expand:
                    columns_to_expand.remove(col)

        expanded_image.append(line)
        if row_empty:
            expanded_image.append("." * len(line))
    for col in sorted(columns_to_expand, reverse=True):
        for row in range(len(expanded_image)):
            expanded_image[row] = (
                expanded_image[row][:col] + "." + expanded_image[row][col:]
            )

    galaxies: list[tuple[int, int]] = []
    for row, line in enumerate(expanded_image):
        for col, pixel in enumerate(expanded_image[row]):
            if pixel == "#":
                galaxies.append((row, col))

    result = 0
    for index, (row, col) in enumerate(galaxies):
        result += sum(abs(row - r) + abs(col - c) for r, c in galaxies[index:])

    return result


def part_two(problem_input: list[str]) -> int:
    expansion_count = 1_000_000

    rows_to_expand = set()
    columns_to_expand = set(range(len(problem_input[0])))
    for row, _ in enumerate(problem_input):
        row_empty = True
        for col, pixel in enumerate(problem_input[row]):
            if pixel == "#":
                row_empty = False
                if col in columns_to_expand:
                    columns_to_expand.remove(col)
        if row_empty:
            rows_to_expand.add(row)

    galaxies: list[tuple[int, int]] = []
    for row, _ in enumerate(problem_input):
        for col, pixel in enumerate(problem_input[row]):
            if pixel == "#":
                galaxies.append((row, col))

    result = 0
    for index, (row, col) in enumerate(galaxies):
        for other_row, other_col in galaxies[index:]:
            distance = 0
            for r in range(min(row, other_row), max(row, other_row)):
                distance += expansion_count if r in rows_to_expand else 1
            for c in range(min(col, other_col), max(col, other_col)):
                distance += expansion_count if c in columns_to_expand else 1

            result += distance

    return result


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
