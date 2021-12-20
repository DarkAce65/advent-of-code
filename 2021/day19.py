from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int


class Scanner:
    number: int
    beacon_positions: set[Vector3]

    def __init__(self, number: int) -> None:
        self.number = number
        self.beacon_positions = set()

    def add_beacon(self, position: Vector3) -> None:
        self.beacon_positions.add(position)


def parse_scanner_report(scanner_report: list[str]) -> list[Scanner]:
    scanners: list[Scanner] = []
    for line in scanner_report:
        if line == "":
            continue
        if "scanner" in line:
            scanners.append(Scanner(int(line.split()[2])))
            line.split()
        else:
            [x, y, z] = line.split(",")
            scanners[-1].add_beacon(Vector3(int(x), int(y), int(z)))

    return scanners


def part_one(scanner_report: list[Scanner]) -> int:
    pass


def part_two(scanner_report: list[Scanner]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    scanner_report = parse_scanner_report(problem_input)

    print("Part One: ", part_one(scanner_report))
    print("Part Two: ", part_two(scanner_report))
