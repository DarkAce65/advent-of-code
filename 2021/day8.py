from typing import Optional, Tuple, cast

from utils import get_and_cache_input

SEGMENT_MAPPING = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def part_one(parsed_display_log: list[Tuple[list[str], list[str]]]) -> int:
    num_unique_outputs = 0
    for entry in parsed_display_log:
        (_, output_digits) = entry
        for digit in output_digits:
            if len(digit) in [2, 3, 4, 7]:
                num_unique_outputs += 1

    return num_unique_outputs


def convert_segments_to_digit(segments: str) -> int:
    return SEGMENT_MAPPING["".join(sorted(segments))]


def identify_segments(signal_values: list[str]) -> dict[str, str]:
    """
    Seven segment display mapping:
     aaaa
    b    c
    b    c
     dddd
    e    f
    e    f
     gggg
    """

    mapping: dict[str, Optional[str]] = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "e": None,
        "f": None,
        "g": None,
    }
    signal_segments = sorted(
        list(map(lambda signal_value: set(signal_value), signal_values)), key=len
    )
    digit_to_segments = {
        1: signal_segments[0],
        4: signal_segments[2],
        7: signal_segments[1],
        8: signal_segments[9],
    }
    digits_235 = signal_segments[3:6]
    digits_069 = signal_segments[6:9]
    for digit_069 in digits_069:
        if len(digit_to_segments[1].intersection(digit_069)) == 1:
            digit_to_segments[6] = digit_069
        elif len(digit_to_segments[4].intersection(digit_069)) == 4:
            digit_to_segments[9] = digit_069
        else:
            digit_to_segments[0] = digit_069
    for digit_235 in digits_235:
        if len(digit_to_segments[6].difference(digit_235)) == 1:
            digit_to_segments[5] = digit_235
        elif len(digit_to_segments[1].intersection(digit_235)) == 2:
            digit_to_segments[3] = digit_235
        else:
            digit_to_segments[2] = digit_235

    mapping[next(iter(digit_to_segments[7].difference(digit_to_segments[1])))] = "a"
    mapping[next(iter(digit_to_segments[5].difference(digit_to_segments[3])))] = "b"
    mapping[next(iter(digit_to_segments[1].difference(digit_to_segments[5])))] = "c"
    mapping[next(iter(digit_to_segments[8].difference(digit_to_segments[0])))] = "d"
    mapping[next(iter(digit_to_segments[6].difference(digit_to_segments[5])))] = "e"
    mapping[next(iter(digit_to_segments[1].difference(digit_to_segments[2])))] = "f"
    mapping[
        next(
            iter(
                digit_to_segments[9]
                .difference(digit_to_segments[4])
                .difference(digit_to_segments[7])
            )
        )
    ] = "g"

    return cast(dict[str, str], mapping)


def part_two(parsed_display_log: list[Tuple[list[str], list[str]]]) -> int:
    output_sum = 0
    for entry in parsed_display_log:
        (signal_values, output_digits) = entry

        mapping = identify_segments(signal_values)
        decoded_output_digits: list[str] = []
        for output_digit in output_digits:
            remapped_output_digit = "".join(mapping[c] for c in output_digit)
            decoded_output_digit = convert_segments_to_digit(remapped_output_digit)
            decoded_output_digits.append(str(decoded_output_digit))

        output_sum += int("".join(decoded_output_digits))

    return output_sum


def parse_entry(entry: str) -> Tuple[list[str], list[str]]:
    [signal_digits, output_digits] = entry.split(" | ")
    return (signal_digits.split(), output_digits.split())


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    parsed_display_log = list(map(parse_entry, problem_input))

    print("Part One: ", part_one(parsed_display_log))
    print("Part Two: ", part_two(parsed_display_log))
