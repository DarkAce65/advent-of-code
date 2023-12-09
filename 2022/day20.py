import math

from utils import get_and_cache_input


def mix(encrypted_file: list[tuple[int, int]]) -> list[tuple[int, int]]:
    decrypted_file = encrypted_file.copy()

    for i, num in sorted(encrypted_file, key=lambda item: item[0]):
        if num == 0:
            continue

        index = decrypted_file.index((i, num))
        decrypted_file.pop(index)

        between_index = index - 0.5
        new_index = int(math.floor(between_index + num + 1)) % len(decrypted_file)

        decrypted_file.insert(new_index, (i, num))

    return decrypted_file


def part_one(problem_input: list[str]) -> int:
    encrypted_file: list[tuple[int, int]] = []
    for i, num in enumerate(problem_input):
        encrypted_file.append((i, int(num)))

    decrypted_file = [num for _, num in mix(encrypted_file)]
    index_of_zero = decrypted_file.index(0)

    return (
        decrypted_file[(index_of_zero + 1000) % len(decrypted_file)]
        + decrypted_file[(index_of_zero + 2000) % len(decrypted_file)]
        + decrypted_file[(index_of_zero + 3000) % len(decrypted_file)]
    )


def part_two(problem_input: list[str]) -> int:
    decryption_key = 811589153

    encrypted_file: list[tuple[int, int]] = []
    for i, num in enumerate(problem_input):
        encrypted_file.append((i, int(num) * decryption_key))

    intermediate_file = mix(encrypted_file)
    for _ in range(9):
        intermediate_file = mix(intermediate_file)

    decrypted_file = [num for _, num in intermediate_file]
    index_of_zero = decrypted_file.index(0)

    return (
        decrypted_file[(index_of_zero + 1000) % len(decrypted_file)]
        + decrypted_file[(index_of_zero + 2000) % len(decrypted_file)]
        + decrypted_file[(index_of_zero + 3000) % len(decrypted_file)]
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
