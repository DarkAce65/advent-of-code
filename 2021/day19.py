from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)


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


def find_offset(
    scanner1: Scanner, scanner2: Scanner, num_overlaps_needed: int
) -> Optional[Vector3]:
    for beacon1 in scanner1.beacon_positions:
        anchor_beacon1 = beacon1
        for beacon2 in scanner2.beacon_positions:
            anchor_beacon2 = beacon2
            offset = anchor_beacon1 - anchor_beacon2

            index = 0
            overlap = 0
            for b in scanner2.beacon_positions:
                if b + offset in scanner1.beacon_positions:
                    overlap += 1
                if overlap >= num_overlaps_needed:
                    return offset
                if (
                    index - overlap
                    >= len(scanner2.beacon_positions) - num_overlaps_needed
                ):
                    break
                index += 1

    return None


def part_one(scanner_report: list[Scanner]) -> int:
    scanner_positions: dict[int, Vector3] = {}
    known_scanners: dict[int, Scanner] = {}
    scanner_positions[scanner_report[0].number] = Vector3(0, 0, 0)
    known_scanners[scanner_report[0].number] = scanner_report[0]

    unknown_scanners = deque(scanner_report[1:])
    last_unplaceable_length: dict[int, int] = {}
    while len(unknown_scanners) > 0:
        scanner = unknown_scanners.popleft()
        for known_scanner in known_scanners.values():
            offset = find_offset(known_scanner, scanner, 3)
            if offset is not None:
                scanner_positions[scanner.number] = (
                    scanner_positions[known_scanner.number] + offset
                )
                known_scanners[scanner.number] = scanner
                if scanner.number in last_unplaceable_length:
                    del last_unplaceable_length[scanner.number]
                break

        if scanner.number not in known_scanners:
            unknown_scanners.append(scanner)
            if scanner.number in last_unplaceable_length and last_unplaceable_length[
                scanner.number
            ] == len(unknown_scanners):
                raise ValueError(
                    f"Unable to locate scanners: {sorted(s.number for s in unknown_scanners)}"
                )
            last_unplaceable_length[scanner.number] = len(unknown_scanners)

    for k, v in sorted(scanner_positions.items()):
        print(k, v)

    return 0


def part_two(scanner_report: list[Scanner]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    scanner_report = parse_scanner_report(problem_input)

    print("Part One: ", part_one(scanner_report))
    print("Part Two: ", part_two(scanner_report))
