from collections import deque
from pathlib import Path


def part_one(digit_candidates: list[set[int]]) -> int:
    model_number = ""
    for candidates in digit_candidates:
        model_number += str(max(candidates))

    return int(model_number)


def part_two(digit_candidates: list[set[int]]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    a_values = [1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 1, 26, 26, 26]
    b_values = [10, 15, 14, 15, -8, 10, -16, -4, 11, -3, 12, -7, -15, -7]
    c_values = [2, 16, 9, 0, 1, 12, 6, 6, 3, 5, 9, 3, 2, 3]

    digit_candidates: list[set[int]] = []
    for _ in range(14):
        digit_candidates.append(set([1, 2, 3, 4, 5, 6, 7, 8, 9]))

    c_stack: deque[int] = deque()
    for index in range(14):
        b = b_values[index]
        if b >= 0:
            c_stack.append(index)
        else:
            prev_c_index = c_stack.pop()
            prev_c = c_values[prev_c_index]
            diff = prev_c + b
            if diff > 0:
                for n in range(10 - diff, 10):
                    if n in digit_candidates[prev_c_index]:
                        digit_candidates[prev_c_index].remove(n)
            else:
                for n in range(1, -diff + 1):
                    if n in digit_candidates[prev_c_index]:
                        digit_candidates[prev_c_index].remove(n)

            digit_candidates[index] = digit_candidates[index].intersection(
                {
                    prev_candidate + diff
                    for prev_candidate in digit_candidates[prev_c_index]
                }
            )

    print("Part One: ", part_one(digit_candidates))
    print("Part Two: ", part_two(digit_candidates))
