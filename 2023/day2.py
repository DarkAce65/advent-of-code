import re
from pathlib import Path


class Game:
    id: int
    rounds: list[dict[str, int]]

    def __init__(self, game_str: str) -> None:
        match = re.match(r"Game (\d+): (.*)", game_str)
        assert match is not None

        self.id = int(match.group(1))
        self.rounds = []
        for round_str in match.group(2).split(";"):
            round = {}
            for cube_pair in round_str.strip().split(","):
                num, color = cube_pair.strip().split(" ")
                round[color] = int(num)
            self.rounds.append(round)

    def compute_power(self) -> int:
        red = max(round.get("red", 0) for round in self.rounds)
        green = max(round.get("green", 0) for round in self.rounds)
        blue = max(round.get("blue", 0) for round in self.rounds)

        return red * green * blue


# 12 red cubes, 13 green cubes, 14 blue cubes
def part_one(games: list[Game]) -> int:
    sum = 0
    for game in games:
        if all(
            round.get("red", 0) <= 12
            and round.get("green", 0) <= 13
            and round.get("blue", 0) <= 14
            for round in game.rounds
        ):
            sum += game.id

    return sum


def part_two(games: list[Game]) -> int:
    return sum(game.compute_power() for game in games)


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    games = [Game(game_str) for game_str in problem_input]

    print("Part One: ", part_one(games))
    print("Part Two: ", part_two(games))
