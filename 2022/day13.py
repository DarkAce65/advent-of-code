import functools
import json
from typing import Union, cast

from utils import get_and_cache_input

Packet = list[int] | list[Union[int, "Packet"]]


# def parse_packet(packet_str: str) -> int | Packet:
#     if packet_str.isdigit():
#         return int(packet_str)

#     brackets = 0
#     packet: Packet = []  # type: ignore
#     sub_packet = ""
#     for c in packet_str:
#         if c == "[":
#             brackets += 1
#         elif c == "]":
#             brackets -= 1

#         if (c == "]" and brackets == 0) or (c == "," and brackets == 1):
#             packet.append(parse_packet(sub_packet))  # type: ignore
#             sub_packet = ""
#         elif not (c == "[" and brackets == 1):
#             sub_packet += c

#     return packet


def parse_packet(packet_str: str) -> Packet:
    return json.loads(packet_str)


def compare_values(left: int | Packet, right: int | Packet) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0
    elif isinstance(left, int):
        return compare_values([left], right)
    elif isinstance(right, int):
        return compare_values(left, [right])

    for l, r in zip(left, right):
        compared = compare_values(l, r)
        if compared == 0:
            continue
        else:
            return compared

    if len(left) < len(right):
        return 1
    elif len(left) > len(right):
        return -1

    return 0


def part_one(problem_input: list[str]) -> int:
    left_packets: list[Packet] = []
    right_packets: list[Packet] = []
    for line in problem_input:
        if len(line) > 0:
            if len(left_packets) <= len(right_packets):
                left_packets.append(parse_packet(line))
            else:
                right_packets.append(parse_packet(line))

    ans = 0
    for i, (left, right) in enumerate(zip(left_packets, right_packets)):
        if compare_values(left, right) == 1:
            ans += i + 1

    return ans


def part_two(problem_input: list[str]) -> int:
    divider_packet1: Packet = cast(Packet, [[2]])
    divider_packet2: Packet = cast(Packet, [[6]])

    packets: list[Packet] = [divider_packet1, divider_packet2]
    for line in problem_input:
        if len(line) > 0:
            packets.append(cast(Packet, parse_packet(line)))

    sorted_packets = sorted(
        packets, key=functools.cmp_to_key(compare_values), reverse=True
    )
    return (sorted_packets.index(divider_packet1) + 1) * (
        sorted_packets.index(divider_packet2) + 1
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
