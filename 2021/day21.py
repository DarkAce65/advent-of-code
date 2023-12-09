
from typing import Counter

from utils import get_and_cache_input

POSSIBLE_ROLLS: list[int] = []
for r1 in range(1, 4):
    for r2 in range(1, 4):
        for r3 in range(1, 4):
            POSSIBLE_ROLLS.append(r1 + r2 + r3)


def parse_starting_positions(problem_input: list[str]) -> list[int]:
    starting_positions = []
    for line in problem_input:
        [_, starting_position] = line.split(":")
        starting_positions.append(int(starting_position.strip()))

    return starting_positions


def part_one(starting_positions: list[int]) -> int:
    positions = starting_positions.copy()
    scores = []
    for _ in positions:
        scores.append(0)

    turn = 0
    roll = 1 + 2 + 3
    num_rolls = 3
    while True:
        positions[turn] = (positions[turn] - 1 + roll) % 10 + 1
        scores[turn] += positions[turn]
        if scores[turn] >= 1000:
            break
        turn = (turn + 1) % len(positions)
        roll += 9
        num_rolls += 3

    return min(scores) * num_rolls


def find_winner_counts(
    positions: list[int], scores: list[int], turn: int = 0
) -> Counter[int]:
    c: Counter[int] = Counter()
    next_turn = (turn + 1) % len(positions)

    for possible_roll in POSSIBLE_ROLLS:
        p = positions.copy()
        s = scores.copy()
        p[turn] = (p[turn] - 1 + possible_roll) % 10 + 1
        s[turn] += p[turn]

        if s[turn] >= 21:
            c += Counter([turn])
        else:
            c += find_winner_counts_cached(p, s, next_turn)

    return c


cache: dict[str, Counter[int]] = {}
cache_stats: list[int] = [0, 0]


def find_winner_counts_cached(
    positions: list[int], scores: list[int], turn: int = 0
) -> Counter[int]:
    cache_key = "".join(map(str, positions)) + "".join(map(str, scores)) + str(turn)
    if cache_key not in cache:
        cache_stats[1] += 1
        cache[cache_key] = find_winner_counts(positions, scores, turn)
    else:
        cache_stats[0] += 1

    return cache[cache_key]


def part_two(starting_positions: list[int]) -> int:
    winner_counts = find_winner_counts_cached(starting_positions, [0, 0])
    return max(winner_counts.values())


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    starting_positions = parse_starting_positions(problem_input)

    print("Part One: ", part_one(starting_positions))
    print("Part Two: ", part_two(starting_positions))
