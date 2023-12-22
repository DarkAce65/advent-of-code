from __future__ import annotations

from collections import defaultdict, namedtuple
from dataclasses import dataclass
from heapq import heapify, heappop, heappush

from utils import get_and_cache_input

Coordinate = namedtuple("Coordinate", ["x", "y", "z"])


@dataclass(frozen=True)
class Brick:
    id: int
    start: Coordinate
    end: Coordinate

    def __lt__(self, other: Brick) -> bool:
        return self.start.z < other.start.z or (
            self.start.z == other.start.z and self.end.z < other.end.z
        )

    def assert_valid(self):
        assert self.start.x <= self.end.x
        assert self.start.y <= self.end.y
        assert self.start.z <= self.end.z

    def could_collide(self, other: Brick) -> bool:
        return (
            other.end.z < self.start.z
            and (
                other.start.x <= self.start.x <= other.end.x
                or other.start.x <= self.end.x <= other.end.x
                or self.start.x <= other.start.x <= other.end.x <= self.end.x
            )
            and (
                other.start.y <= self.start.y <= other.end.y
                or other.start.y <= self.end.y <= other.end.y
                or self.start.y <= other.start.y <= other.end.y <= self.end.y
            )
        )


def settle_bricks(
    bricks: list[Brick],
) -> tuple[list[Brick], dict[int, set[int]], dict[int, set[int]]]:
    unstable_bricks: list[Brick] = bricks.copy()
    stable_bricks: list[Brick] = []
    supported_bricks_by_id: dict[int, set[int]] = defaultdict(set)
    heapify(unstable_bricks)

    while len(unstable_bricks) > 0:
        brick = heappop(unstable_bricks)
        if brick.start.z == 1:
            stable_bricks.append(brick)
            continue

        highest_z = 0
        is_stable = False
        collided_with: list[Brick] = []
        for unstable_brick in unstable_bricks:
            if highest_z <= unstable_brick.end.z and brick.could_collide(unstable_brick):
                if highest_z == unstable_brick.end.z:
                    collided_with.append(unstable_brick)
                else:
                    collided_with = [unstable_brick]
                highest_z = unstable_brick.end.z
                is_stable = False
        for stable_brick in stable_bricks:
            if highest_z <= stable_brick.end.z and brick.could_collide(stable_brick):
                if highest_z == stable_brick.end.z:
                    collided_with.append(stable_brick)
                else:
                    collided_with = [stable_brick]
                highest_z = stable_brick.end.z
                is_stable = True

        supported_bricks_by_id[brick.id].clear()
        for b in collided_with:
            supported_bricks_by_id[b.id].add(brick.id)

        moved_brick = Brick(
            brick.id,
            Coordinate(brick.start.x, brick.start.y, highest_z + 1),
            Coordinate(
                brick.end.x,
                brick.end.y,
                highest_z + 1 + brick.end.z - brick.start.z,
            ),
        )

        if is_stable or collided_with is None:
            stable_bricks.append(moved_brick)
        else:
            heappush(unstable_bricks, moved_brick)

    supporting_bricks_by_id: dict[int, set[int]] = defaultdict(set)
    for brick_id, supported_ids in supported_bricks_by_id.items():
        for b_id in supported_ids:
            supporting_bricks_by_id[b_id].add(brick_id)

    return (stable_bricks, supported_bricks_by_id, supporting_bricks_by_id)


def find_non_critical_bricks(
    settled_bricks: list[Brick],
    supported_bricks_by_id: dict[int, set[int]],
    supporting_bricks_by_id: dict[int, set[int]],
) -> dict[int, bool]:
    non_critical_bricks: dict[int, bool] = {}
    for brick in settled_bricks:
        if len(supported_bricks_by_id[brick.id]) == 0:
            non_critical_bricks[brick.id] = True

        if len(supporting_bricks_by_id[brick.id]) < 2:
            for b_id in supporting_bricks_by_id[brick.id]:
                non_critical_bricks[b_id] = False
        else:
            for b_id in supporting_bricks_by_id[brick.id]:
                if b_id not in non_critical_bricks:
                    non_critical_bricks[b_id] = True

    return non_critical_bricks


def part_one(
    settled_bricks: list[Brick],
    supported_bricks_by_id: dict[int, set[int]],
    supporting_bricks_by_id: dict[int, set[int]],
) -> int:
    return sum(
        1
        for can_disintegrate in find_non_critical_bricks(
            settled_bricks, supported_bricks_by_id, supporting_bricks_by_id
        ).values()
        if can_disintegrate
    )


def count_cascading_bricks(
    supported_bricks_by_id: dict[int, set[int]],
    supporting_bricks_by_id: dict[int, set[int]],
    initial_brick_id: int,
) -> set[int]:
    cascaded_bricks: set[int] = set([initial_brick_id])

    to_visit: set[int] = set([initial_brick_id])
    while len(to_visit) > 0:
        brick_id = to_visit.pop()

        if len(supporting_bricks_by_id[brick_id].difference(cascaded_bricks)) == 0:
            cascaded_bricks.add(brick_id)

        for supported_brick_id in supported_bricks_by_id[brick_id]:
            to_visit.add(supported_brick_id)

    return cascaded_bricks


def part_two(
    settled_bricks: list[Brick],
    supported_bricks_by_id: dict[int, set[int]],
    supporting_bricks_by_id: dict[int, set[int]],
) -> int:
    result = 0
    for brick in settled_bricks:
        result += (
            len(
                count_cascading_bricks(
                    supported_bricks_by_id, supporting_bricks_by_id, brick.id
                )
            )
            - 1
        )
    return result


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    bricks: list[Brick] = []
    for index, line in enumerate(problem_input):
        start, end = line.split("~")
        brick = Brick(
            index,
            Coordinate(*[int(v) for v in start.split(",")]),
            Coordinate(*[int(v) for v in end.split(",")]),
        )
        brick.assert_valid()
        bricks.append(brick)

    settled_bricks, supported_bricks_by_id, supporting_bricks_by_id = settle_bricks(
        bricks
    )

    print(
        "Part One: ",
        part_one(settled_bricks, supported_bricks_by_id, supporting_bricks_by_id),
    )
    print(
        "Part Two: ",
        part_two(settled_bricks, supported_bricks_by_id, supporting_bricks_by_id),
    )
