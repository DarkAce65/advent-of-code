from utils import get_and_cache_input


def snafu_digit_to_decimal(snafu_digit: str) -> int:
    if snafu_digit.isdigit():
        return int(snafu_digit)
    elif snafu_digit == "-":
        return -1
    elif snafu_digit == "=":
        return -2
    else:
        raise ValueError("Unrecognized SNAFU number `" + snafu_digit + "`")


def decimal_digit_to_snafu(num: int) -> str:
    assert -2 <= num <= 2
    if num == -2:
        return "="
    elif num == -1:
        return "-"
    else:
        return str(num)


def add_snafu_numbers(num1: str, num2: str) -> str:
    result = ""
    length = max(len(num1), len(num2))
    carryover = 0
    for l, r in zip(reversed(num1.rjust(length, "0")), reversed(num2.rjust(length, "0"))):
        digit = snafu_digit_to_decimal(l) + snafu_digit_to_decimal(r) + carryover
        if digit > 2:
            snafu_digit = decimal_digit_to_snafu(digit - 5)
            carryover = 1
        elif digit < -2:
            snafu_digit = decimal_digit_to_snafu(digit + 5)
            carryover = -1
        else:
            snafu_digit = decimal_digit_to_snafu(digit)
            carryover = 0
        result = snafu_digit + result

    if carryover != 0:
        result = decimal_digit_to_snafu(carryover) + result

    return result


def part_one(problem_input: list[str]) -> str:
    num = ""
    for line in problem_input:
        num = add_snafu_numbers(num, line)
    return num


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
