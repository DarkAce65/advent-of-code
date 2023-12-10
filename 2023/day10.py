from utils import get_and_cache_input

Position = tuple[int, int]


def get_next_position(
    pipes: dict[Position, set[Position]], tile: Position, prev_tile: Position
) -> Position:
    assert len(pipes[tile]) == 2 and prev_tile in pipes[tile]
    return [t for t in pipes[tile] if t != prev_tile][0]


def build_pipes(
    problem_input: list[str],
) -> tuple[Position, dict[Position, set[Position]]]:
    start_position: Position | None = None
    pipes: dict[Position, set[Position]] = {}
    for row, line in enumerate(problem_input):
        for col, tile in enumerate(line):
            position = (row, col)
            if tile == "S":
                start_position = position
                pipes[position] = set()
                if row > 0 and (
                    problem_input[row - 1][col] == "|"
                    or problem_input[row - 1][col] == "7"
                    or problem_input[row - 1][col] == "F"
                ):
                    pipes[position].add((row - 1, col))
                if col > 0 and (
                    problem_input[row][col - 1] == "-"
                    or problem_input[row][col - 1] == "L"
                    or problem_input[row][col - 1] == "F"
                ):
                    pipes[position].add((row, col - 1))
                if col + 1 < len(problem_input[row]) and (
                    problem_input[row][col + 1] == "-"
                    or problem_input[row][col + 1] == "J"
                    or problem_input[row][col + 1] == "7"
                ):
                    pipes[position].add((row, col + 1))
                if row + 1 < len(problem_input) and (
                    problem_input[row + 1][col] == "|"
                    or problem_input[row + 1][col] == "L"
                    or problem_input[row + 1][col] == "J"
                ):
                    pipes[position].add((row + 1, col))
            elif tile == "|":
                pipes[position] = set([(row - 1, col), (row + 1, col)])
            elif tile == "-":
                pipes[position] = set([(row, col - 1), (row, col + 1)])
            elif tile == "L":
                pipes[position] = set([(row - 1, col), (row, col + 1)])
            elif tile == "J":
                pipes[position] = set([(row - 1, col), (row, col - 1)])
            elif tile == "7":
                pipes[position] = set([(row, col - 1), (row + 1, col)])
            elif tile == "F":
                pipes[position] = set([(row, col + 1), (row + 1, col)])

    assert start_position is not None

    return (start_position, pipes)


def part_one(problem_input: list[str]) -> int:
    start_position, pipes = build_pipes(problem_input)

    one, two = pipes[start_position]
    path_one: list[Position] = [start_position, one]
    path_two: list[Position] = [start_position, two]
    while path_one[-1] != path_two[-1]:
        path_one.append(get_next_position(pipes, path_one[-1], path_one[-2]))
        path_two.append(get_next_position(pipes, path_two[-1], path_two[-2]))

    return len(path_one) - 1


def find_is_inside(
    walls: set[Position],
    position: Position,
    inside_positions: set[Position],
    outside_positions: set[Position],
) -> tuple[bool, set[Position]]:
    max_row = 0
    max_col = 0
    for row, col in walls:
        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col

    to_visit: list[Position] = [position]
    visited: set[Position] = set()
    while len(to_visit) > 0:
        current = to_visit.pop()
        visited.add(current)
        if current in inside_positions:
            return (True, visited.union(to_visit))
        elif (
            current in outside_positions
            or current[0] == 0
            or current[0] >= max_row
            or current[1] == 0
            or current[1] >= max_col
        ):
            return (False, visited.union(to_visit))
        else:
            row, col = current
            if (row - 1, col) not in walls and (row - 1, col) not in visited:
                to_visit.append((row - 1, col))
            if (row, col - 1) not in walls and (row, col - 1) not in visited:
                to_visit.append((row, col - 1))
            if (row, col + 1) not in walls and (row, col + 1) not in visited:
                to_visit.append((row, col + 1))
            if (row + 1, col) not in walls and (row + 1, col) not in visited:
                to_visit.append((row + 1, col))

    return (True, visited)


def part_two(problem_input: list[str]) -> int:
    start_position, pipes = build_pipes(problem_input)

    (one, _) = pipes[start_position]
    path: list[Position] = [start_position, one]
    while True:
        next_position = get_next_position(pipes, path[-1], path[-2])
        if next_position == start_position:
            break
        path.append(next_position)

    non_path: set[Position] = set()
    for row in range(len(problem_input)):
        for col in range(len(problem_input[row])):
            if (row, col) not in path:
                non_path.add((row, col))

    path_scaled: set[Position] = set()
    non_path_scaled: set[Position] = {(row * 2, col * 2) for row, col in non_path}
    for row, col in path:
        path_scaled.add((row * 2, col * 2))
        if (row, col + 1) in pipes[(row, col)]:
            path_scaled.add((row * 2, col * 2 + 1))
        if (row + 1, col) in pipes[(row, col)]:
            path_scaled.add((row * 2 + 1, col * 2))

    inside_positions: set[Position] = set()
    outside_positions: set[Position] = set()
    to_visit: set[Position] = non_path_scaled.copy()
    while len(to_visit) > 0:
        position = to_visit.pop()
        is_inside, positions = find_is_inside(
            path_scaled, position, inside_positions, outside_positions
        )
        if is_inside:
            inside_positions.update(positions)
        else:
            outside_positions.update(positions)
    return len(non_path_scaled.intersection(inside_positions))


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
