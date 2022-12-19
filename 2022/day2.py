from pathlib import Path
from typing import Literal, Union


def player_score(player: str) -> int:
    if player == "X":
        return 1
    elif player == "Y":
        return 2
    elif player == "Z":
        return 3

    raise ValueError


def evaluate(opponent: str, player: str) -> tuple[int, int]:
    if opponent == "A":
        if player == "X":
            return (3, player_score(player))
        elif player == "Y":
            return (6, player_score(player))
        elif player == "Z":
            return (0, player_score(player))
    elif opponent == "B":
        if player == "X":
            return (0, player_score(player))
        elif player == "Y":
            return (3, player_score(player))
        elif player == "Z":
            return (6, player_score(player))
    elif opponent == "C":
        if player == "X":
            return (6, player_score(player))
        elif player == "Y":
            return (0, player_score(player))
        elif player == "Z":
            return (3, player_score(player))

    raise ValueError


def compute_outcome(opponent: str, outcome: str) -> str:
    if opponent == "A":
        if outcome == "X":
            return "Z"
        elif outcome == "Y":
            return "X"
        elif outcome == "Z":
            return "Y"
    elif opponent == "B":
        if outcome == "X":
            return "X"
        elif outcome == "Y":
            return "Y"
        elif outcome == "Z":
            return "Z"
    elif opponent == "C":
        if outcome == "X":
            return "Y"
        elif outcome == "Y":
            return "Z"
        elif outcome == "Z":
            return "X"

    raise ValueError


def part_one(problem_input: list[str]) -> int:
    score = 0
    for game in problem_input:
        opponent, player = game.split(" ")
        game_score, choice_score = evaluate(opponent, player)
        score += game_score + choice_score

    return score


def part_two(problem_input: list[str]) -> int:
    score = 0
    for game in problem_input:
        opponent, outcome = game.split(" ")
        player = compute_outcome(opponent, outcome)
        game_score, choice_score = evaluate(opponent, player)
        score += game_score + choice_score

    return score


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
