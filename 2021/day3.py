from utils import get_and_cache_input


def part_one(report_values: list[str]) -> int:
    occurrences = [0] * len(report_values[0])
    for report_value in report_values:
        for i in range(len(occurrences)):
            if report_value[i] == "1":
                occurrences[i] += 1

    gamma_rate_binary = "".join(
        "1" if value > len(report_values) / 2 else "0" for value in occurrences
    )
    epsilon_rate_binary = "".join("1" if c == "0" else "0" for c in gamma_rate_binary)
    gamma_rate = int(
        gamma_rate_binary,
        2,
    )
    epsilon_rate = int(
        epsilon_rate_binary,
        2,
    )

    return gamma_rate * epsilon_rate


def part_two(report_values: list[str]) -> int:
    (oxygen_rating_candidates, co2_rating_candidates) = (
        report_values.copy(),
        report_values.copy(),
    )
    oxygen_rating_check_bit = 0
    while len(oxygen_rating_candidates) > 1 and oxygen_rating_check_bit < len(
        report_values[0]
    ):
        occurrences = 0
        for oxygen_rating_candidate in oxygen_rating_candidates:
            if oxygen_rating_candidate[oxygen_rating_check_bit] == "1":
                occurrences += 1
        if occurrences >= len(oxygen_rating_candidates) / 2:
            oxygen_rating_candidates = list(
                filter(
                    lambda candidate: candidate[oxygen_rating_check_bit] == "1",
                    oxygen_rating_candidates,
                )
            )
        else:
            oxygen_rating_candidates = list(
                filter(
                    lambda candidate: candidate[oxygen_rating_check_bit] == "0",
                    oxygen_rating_candidates,
                )
            )
        oxygen_rating_check_bit += 1

    co2_rating_check_bit = 0
    while len(co2_rating_candidates) > 1 and co2_rating_check_bit < len(report_values[0]):
        occurrences = 0
        for co2_rating_candidate in co2_rating_candidates:
            if co2_rating_candidate[co2_rating_check_bit] == "1":
                occurrences += 1
        if occurrences < len(co2_rating_candidates) / 2:
            co2_rating_candidates = list(
                filter(
                    lambda candidate: candidate[co2_rating_check_bit] == "1",
                    co2_rating_candidates,
                )
            )
        else:
            co2_rating_candidates = list(
                filter(
                    lambda candidate: candidate[co2_rating_check_bit] == "0",
                    co2_rating_candidates,
                )
            )
        co2_rating_check_bit += 1

    return int(oxygen_rating_candidates[0], 2) * int(co2_rating_candidates[0], 2)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
