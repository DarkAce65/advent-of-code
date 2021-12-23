from collections import deque
from pathlib import Path
from typing import Literal, Optional, Union


class Burrow:
    rooms: list[deque[str]]
    hallway_slots: list[Optional[str]]

    def __init__(self, problem_input: list[str]) -> None:
        self.rooms = []
        for index in range(len(problem_input[2])):
            if problem_input[2][index].isalpha():
                self.rooms.append(deque(problem_input[2][index]))

        for row in problem_input[3:]:
            parsed_row = row.strip().replace("#", "")
            for index in range(len(parsed_row)):
                self.rooms[index].append(parsed_row[index])

        self.hallway_slots = [None] * (len(problem_input[1].strip("#")) - len(self.rooms))

    def __repr__(self) -> str:
        return "rooms: " + str(self.rooms) + "\nhallway: " + str(self.hallway_slots)


def part_one(problem_input: list[str]) -> int:
    burrow = Burrow(problem_input)

    print(burrow)

    return 0


def part_two(problem_input: list[str]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
