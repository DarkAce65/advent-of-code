import itertools
from pathlib import Path
from typing import Iterable, Iterator, Optional, Sequence, TypeVar

ROOM_INDEX_TO_AMPHIPOD = {0: "A", 1: "B", 2: "C", 3: "D"}
AMPHIPOD_TO_ROOM_INDEX = {v: k for k, v in ROOM_INDEX_TO_AMPHIPOD.items()}
AMPHIPOD_STEP_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


T = TypeVar("T")


def chunks(iterable: Iterable[T], chunk_size: int) -> Iterator[list[T]]:
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if len(chunk) == 0:
            return
        yield chunk


def build_burrow_str(
    rooms: Sequence[list[Optional[str]]], hallway_slots: Sequence[Optional[str]]
) -> str:
    s = ""
    for room in rooms:
        s += "".join(map(lambda slot: slot or ".", room))
    s += "|"
    s += "".join(map(lambda slot: slot or ".", hallway_slots))

    return s


def parse_burrow_str(
    burrow_str: str,
) -> tuple[list[list[Optional[str]]], list[Optional[str]]]:
    [rooms_str, hallway_str] = burrow_str.split("|")

    return (
        list(chunks(map(lambda c: None if c == "." else c, rooms_str), 2)),
        list(map(lambda c: None if c == "." else c, hallway_str)),
    )


def parse_input(problem_input: list[str]) -> str:
    rooms: list[list[Optional[str]]] = []
    for index in range(len(problem_input[2])):
        if problem_input[2][index].isalpha():
            rooms.append(list(problem_input[2][index]))

    for row in problem_input[3:]:
        parsed_row = row.strip().replace("#", "")
        for index in range(len(parsed_row)):
            rooms[index].append(parsed_row[index])

    hallway_slots = [None] * (len(problem_input[1].strip("#")) - len(rooms))

    return build_burrow_str(rooms, hallway_slots)


lowest_costs: dict[str, Optional[int]] = {}
lowest_costs[
    build_burrow_str([["A"] * 2, ["B"] * 2, ["C"] * 2, ["D"] * 2], [None] * 7)
] = 0


def compute_best_energy_cost(burrow_str: str) -> Optional[int]:
    if burrow_str in lowest_costs:
        return lowest_costs[burrow_str]

    (rooms, hallway) = parse_burrow_str(burrow_str)

    next_states: list[tuple[str, int]] = []

    for hallway_index in range(len(hallway)):
        amphipod = hallway[hallway_index]
        if amphipod is None:
            continue

        room_index = AMPHIPOD_TO_ROOM_INDEX[amphipod]

        target_index_within_room: Optional[int] = None
        for index_within_room in range(len(rooms[room_index])):
            a = rooms[room_index][index_within_room]
            if a is None:
                target_index_within_room = index_within_room
            elif a != amphipod:
                target_index_within_room = None
                break

        if target_index_within_room is None:
            continue

        if room_index + 2 > hallway_index:
            hallway_start_index = hallway_index + 1
            hallway_end_index = room_index + 2
        else:
            hallway_start_index = room_index + 2
            hallway_end_index = hallway_index

        if any(
            slot is not None for slot in hallway[hallway_start_index:hallway_end_index]
        ):
            continue

        next_rooms = rooms.copy()
        next_rooms[room_index][target_index_within_room] = amphipod
        next_hallway = hallway.copy()
        next_hallway[hallway_index] = None

        room_steps = target_index_within_room + 1
        hallway_steps = (hallway_end_index - hallway_start_index) * 2 + 1
        if hallway_index == 0:
            hallway_steps -= 1
        elif hallway_index == 6:
            hallway_steps -= 1

        next_states.append(
            (
                build_burrow_str(next_rooms, next_hallway),
                AMPHIPOD_STEP_COSTS[amphipod] * (room_steps + hallway_steps),
            )
        )

    for room_index in range(len(rooms)):
        room = rooms[room_index]
        if all(
            amphipod is None or amphipod == ROOM_INDEX_TO_AMPHIPOD[room_index]
            for amphipod in room
        ):
            continue

        for amphipod in room:
            if amphipod is None:
                continue

            print("room", amphipod)
            break

    lowest_cost: Optional[int] = None
    for (next_state, cost) in next_states:
        cost_to_organize = compute_best_energy_cost(next_state)
        if cost_to_organize is not None and (
            lowest_cost is None or cost + cost_to_organize < lowest_cost
        ):
            lowest_cost = cost + cost_to_organize

    lowest_costs[burrow_str] = lowest_cost
    return lowest_cost


def part_one(problem_input: list[str]) -> int:
    burrow_str = parse_input(problem_input)
    burrow_str = "BACDBC.A|D......"

    lowest_cost = compute_best_energy_cost(burrow_str)
    if lowest_cost is None:
        raise ValueError("No solution to the given input")

    return lowest_cost


def part_two(problem_input: list[str]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
