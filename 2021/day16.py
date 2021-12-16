from abc import ABC
from pathlib import Path
from typing import Optional

HEX_TO_BINARY = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def convert_hex_to_binary(message: str) -> str:
    return "".join(HEX_TO_BINARY[c] for c in message)


class Packet(ABC):
    version: int
    type_id: int
    value: int

    def __init__(self, version: int, type_id: int, value: int) -> None:
        self.version = version
        self.type_id = type_id
        self.value = value


class LiteralPacket(Packet):
    def __init__(self, version: int, value: int) -> None:
        super().__init__(version, 4, value)

    def __repr__(self) -> str:
        return (
            "Literal(v"
            + str(self.version)
            + ", type_id: "
            + str(self.type_id)
            + ", value: "
            + str(self.value)
            + ")"
        )


class OperatorPacket(Packet):
    sub_packets: list[Packet]

    def __init__(self, version: int, type_id: int, sub_packets: list[Packet]) -> None:
        super().__init__(
            version, type_id, OperatorPacket.compute_value(type_id, sub_packets)
        )
        self.sub_packets = sub_packets

    @staticmethod
    def compute_value(type_id: int, sub_packets: list[Packet]) -> int:
        if type_id == 0:
            return sum(sub_packet.value for sub_packet in sub_packets)
        elif type_id == 1:
            product = 1
            for sub_packet in sub_packets:
                product *= sub_packet.value
            return product
        elif type_id == 2:
            return min(sub_packet.value for sub_packet in sub_packets)
        elif type_id == 3:
            return max(sub_packet.value for sub_packet in sub_packets)
        elif type_id == 5:
            return int(sub_packets[0].value > sub_packets[1].value)
        elif type_id == 6:
            return int(sub_packets[0].value < sub_packets[1].value)
        elif type_id == 7:
            return int(sub_packets[0].value == sub_packets[1].value)

        raise ValueError(f"Unknown type_id {type_id}")

    def __repr__(self) -> str:
        return (
            "Operator(v"
            + str(self.version)
            + ", type_id: "
            + str(self.type_id)
            + ", sub_packets: "
            + str(self.sub_packets)
            + ")"
        )


def parse_packet(binary_message: str) -> tuple[Packet, str]:
    packet: Optional[Packet] = None

    version = int(binary_message[0:3], 2)
    type_id = int(binary_message[3:6], 2)
    data = binary_message[6:]
    remaining_data = data

    if type_id == 4:
        value = ""
        index = 0
        while index + 5 <= len(data):
            block_start_bit = int(data[index], 2)
            value += data[index + 1 : index + 5]
            index += 5

            if block_start_bit == 0:
                break

        packet = LiteralPacket(version, int(value, 2))
        remaining_data = data[index:]
    else:
        length_type_id = int(data[0], 2)
        sub_packets = []

        if length_type_id == 0:
            sub_packets_bit_length = int(data[1:16], 2)
            remaining_data = data[16 + sub_packets_bit_length :]
            data = data[16 : 16 + sub_packets_bit_length]

            while len(data) > 6:
                (sub_packet, data) = parse_packet(data)
                sub_packets.append(sub_packet)
        else:
            num_sub_packets = int(data[1:12], 2)
            data = data[12:]

            while len(data) > 6 and len(sub_packets) < num_sub_packets:
                (sub_packet, data) = parse_packet(data)
                sub_packets.append(sub_packet)

            remaining_data = data

        packet = OperatorPacket(version, type_id, sub_packets)

    if packet is None:
        raise ValueError("Unable to parse message")

    return (packet, remaining_data)


def sum_version_numbers(packet: Packet) -> int:
    if isinstance(packet, OperatorPacket):
        return packet.version + sum(map(sum_version_numbers, packet.sub_packets))

    return packet.version


def part_one(packet: Packet) -> int:
    return sum_version_numbers(packet)


def part_two(packet: Packet) -> int:
    return packet.value


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    (packet, _) = parse_packet(convert_hex_to_binary(problem_input[0]))

    print("Part One: ", part_one(packet))
    print("Part Two: ", part_two(packet))
