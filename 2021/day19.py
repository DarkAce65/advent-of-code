from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Optional


@unique
class AxisDir(str, Enum):
    POS_X = "+x"
    POS_Y = "+y"
    POS_Z = "+z"
    NEG_X = "-x"
    NEG_Y = "-y"
    NEG_Z = "-z"

    def is_positive(self) -> bool:
        return self == AxisDir.POS_X or self == AxisDir.POS_Y or self == AxisDir.POS_Z

    def is_negative(self) -> bool:
        return not self.is_positive()

    def is_x(self) -> bool:
        return self == AxisDir.POS_X or self == AxisDir.NEG_X

    def is_y(self) -> bool:
        return self == AxisDir.POS_Y or self == AxisDir.NEG_Y

    def is_z(self) -> bool:
        return self == AxisDir.POS_Z or self == AxisDir.NEG_Z


@dataclass(frozen=True)
class Orientation:
    forward: AxisDir
    up: AxisDir

    def __repr__(self) -> str:
        return "[" + self.forward + " " + self.up + "]"


DEFAULT_ORIENTATION = Orientation(AxisDir.POS_X, AxisDir.POS_Y)
ALL_ORIENTATIONS = [
    Orientation(AxisDir.POS_X, AxisDir.POS_Y),
    Orientation(AxisDir.POS_X, AxisDir.NEG_Y),
    Orientation(AxisDir.POS_X, AxisDir.POS_Z),
    Orientation(AxisDir.POS_X, AxisDir.NEG_Z),
    Orientation(AxisDir.NEG_X, AxisDir.POS_Y),
    Orientation(AxisDir.NEG_X, AxisDir.NEG_Y),
    Orientation(AxisDir.NEG_X, AxisDir.POS_Z),
    Orientation(AxisDir.NEG_X, AxisDir.NEG_Z),
    Orientation(AxisDir.POS_Y, AxisDir.POS_X),
    Orientation(AxisDir.POS_Y, AxisDir.NEG_X),
    Orientation(AxisDir.POS_Y, AxisDir.POS_Z),
    Orientation(AxisDir.POS_Y, AxisDir.NEG_Z),
    Orientation(AxisDir.NEG_Y, AxisDir.POS_X),
    Orientation(AxisDir.NEG_Y, AxisDir.NEG_X),
    Orientation(AxisDir.NEG_Y, AxisDir.POS_Z),
    Orientation(AxisDir.NEG_Y, AxisDir.NEG_Z),
    Orientation(AxisDir.POS_Z, AxisDir.POS_X),
    Orientation(AxisDir.POS_Z, AxisDir.NEG_X),
    Orientation(AxisDir.POS_Z, AxisDir.POS_Y),
    Orientation(AxisDir.POS_Z, AxisDir.NEG_Y),
    Orientation(AxisDir.NEG_Z, AxisDir.POS_X),
    Orientation(AxisDir.NEG_Z, AxisDir.NEG_X),
    Orientation(AxisDir.NEG_Z, AxisDir.POS_Y),
    Orientation(AxisDir.NEG_Z, AxisDir.NEG_Y),
]


@dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def transform(self, orientation: Orientation) -> Vector3:
        x = self.x
        y = self.y
        z = self.z
        forward = orientation.forward
        up = orientation.up

        if forward.is_x():
            if up.is_y():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(x, y, z)
                    else:
                        return Vector3(x, -y, -z)
                else:
                    if up.is_positive():
                        return Vector3(-x, y, -z)
                    else:
                        return Vector3(-x, -y, z)
            elif up.is_z():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(x, -z, y)
                    else:
                        return Vector3(x, z, -y)
                else:
                    if up.is_positive():
                        return Vector3(-x, z, y)
                    else:
                        return Vector3(-x, -z, -y)
        elif forward.is_y():
            if up.is_x():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(y, x, -z)
                    else:
                        return Vector3(-y, x, z)
                else:
                    if up.is_positive():
                        return Vector3(y, -x, z)
                    else:
                        return Vector3(-y, -x, -z)
            elif up.is_z():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(z, x, y)
                    else:
                        return Vector3(-z, x, -y)
                else:
                    if up.is_positive():
                        return Vector3(-z, -x, y)
                    else:
                        return Vector3(z, -x, -y)
        elif forward.is_z():
            if up.is_x():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(y, z, x)
                    else:
                        return Vector3(-y, -z, x)
                else:
                    if up.is_positive():
                        return Vector3(y, -z, -x)
                    else:
                        return Vector3(-y, z, -x)
            elif up.is_y():
                if forward.is_positive():
                    if up.is_positive():
                        return Vector3(-z, y, x)
                    else:
                        return Vector3(z, -y, x)
                else:
                    if up.is_positive():
                        return Vector3(z, y, -x)
                    else:
                        return Vector3(-z, -y, -x)

        raise ValueError("Unrecognized orientation", orientation)


class Scanner:
    number: int
    beacon_positions: set[Vector3]

    def __init__(self, number: int) -> None:
        self.number = number
        self.beacon_positions = set()

    def add_beacon(self, position: Vector3) -> None:
        self.beacon_positions.add(position)

    def get_world_transformed_beacons(self, orientation: Orientation) -> set[Vector3]:
        return {beacon.transform(orientation) for beacon in self.beacon_positions}


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


def find_offset_and_orientation(
    oriented_scanner1_beacons: set[Vector3], scanner2: Scanner, num_overlaps_needed: int
) -> Optional[tuple[Vector3, Orientation]]:
    for orientation in ALL_ORIENTATIONS:
        for beacon1 in oriented_scanner1_beacons:
            anchor_beacon1 = beacon1
            scanner2_beacons = scanner2.get_world_transformed_beacons(orientation)
            for beacon2 in scanner2_beacons:
                anchor_beacon2 = beacon2
                offset = anchor_beacon1 - anchor_beacon2

                index = 0
                overlap = 0
                for b in scanner2_beacons:
                    if b + offset in oriented_scanner1_beacons:
                        overlap += 1
                    if overlap >= num_overlaps_needed:
                        return (offset, orientation)
                    if index - overlap >= len(scanner2_beacons) - num_overlaps_needed:
                        break
                    index += 1

    return None


def part_one(scanner_report: list[Scanner]) -> int:
    scanner_positions: dict[int, tuple[Vector3, Orientation]] = {}
    known_scanners: dict[int, Scanner] = {}
    scanner_positions[scanner_report[0].number] = (Vector3(0, 0, 0), DEFAULT_ORIENTATION)
    known_scanners[scanner_report[0].number] = scanner_report[0]

    unknown_scanners = deque(scanner_report[1:])
    last_unplaceable_length: dict[int, int] = {}
    while len(unknown_scanners) > 0:
        scanner = unknown_scanners.popleft()
        for known_scanner in known_scanners.values():
            (known_scanner_offset, known_scanner_orientation) = scanner_positions[
                known_scanner.number
            ]
            offset_orientation = find_offset_and_orientation(
                known_scanner.get_world_transformed_beacons(known_scanner_orientation),
                scanner,
                12,
            )
            if offset_orientation is not None:
                (offset, orientation) = offset_orientation
                print(
                    f"{known_scanner.number}<-{scanner.number}",
                    known_scanner_offset + offset,
                    orientation,
                )
                scanner_positions[scanner.number] = (
                    known_scanner_offset + offset,
                    orientation,
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

    all_beacons: set[Vector3] = set()
    for (
        scanner_number,
        (scanner_position, scanner_orientation),
    ) in scanner_positions.items():
        for world_beacon in known_scanners[scanner_number].get_world_transformed_beacons(
            scanner_orientation
        ):
            all_beacons.add(world_beacon + scanner_position)

    return len(all_beacons)


def part_two(scanner_report: list[Scanner]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    scanner_report = parse_scanner_report(problem_input)

    print("Part One: ", part_one(scanner_report))
    print("Part Two: ", part_two(scanner_report))
