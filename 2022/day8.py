from utils import get_and_cache_input


def part_one(problem_input: list[str]) -> int:
    num_visible_trees = len(problem_input[0]) * 2 + len(problem_input) * 2 - 4

    for i, row in enumerate(problem_input):
        if i == 0 or i == len(problem_input) - 1:
            continue
        for j, col in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            cell = int(problem_input[i][j])
            visible_from_top = True
            for k in range(i - 1, -1, -1):
                if int(problem_input[k][j]) >= cell:
                    visible_from_top = False
                    break

            if visible_from_top:
                num_visible_trees += 1
                continue

            visible_from_bottom = True
            for k in range(i + 1, len(problem_input)):
                if int(problem_input[k][j]) >= cell:
                    visible_from_bottom = False
                    break

            if visible_from_bottom:
                num_visible_trees += 1
                continue

            visible_from_left = True
            for k in range(j - 1, -1, -1):
                if int(problem_input[i][k]) >= cell:
                    visible_from_left = False
                    break

            if visible_from_left:
                num_visible_trees += 1
                continue

            visible_from_right = True
            for k in range(j + 1, len(problem_input[i])):
                if int(problem_input[i][k]) >= cell:
                    visible_from_right = False
                    break

            if visible_from_right:
                num_visible_trees += 1
                continue

    return num_visible_trees


def part_two(problem_input: list[str]) -> int:
    best_distance = 0

    for i, row in enumerate(problem_input):
        if i == 0 or i == len(problem_input) - 1:
            continue
        for j, col in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            cell = int(problem_input[i][j])
            range_to_top = 0
            for k in range(i - 1, -1, -1):
                range_to_top += 1
                if int(problem_input[k][j]) >= cell:
                    break
            range_to_bottom = 0
            for k in range(i + 1, len(problem_input)):
                range_to_bottom += 1
                if int(problem_input[k][j]) >= cell:
                    break
            range_to_left = 0
            for k in range(j - 1, -1, -1):
                range_to_left += 1
                if int(problem_input[i][k]) >= cell:
                    break
            range_to_right = 0
            for k in range(j + 1, len(problem_input[i])):
                range_to_right += 1
                if int(problem_input[i][k]) >= cell:
                    break

            distance = range_to_top * range_to_bottom * range_to_left * range_to_right
            if best_distance < distance:
                best_distance = distance

    return best_distance


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
