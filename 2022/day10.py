from typing import Callable

from utils import get_and_cache_input


def execute_program(problem_input: list[str], cycle_hook: Callable[[int, int], None]):
    current_cycle = 0
    program_counter = -1

    register_value = 1

    current_instruction: tuple[str, int] = ("", 0)

    while True:
        cycle_hook(current_cycle, register_value)

        if current_instruction[1] == 0:
            instr = current_instruction[0]
            if instr == "noop":
                pass
            elif instr.startswith("addx"):
                inc = int(instr.split(" ")[1])
                register_value += inc

            program_counter += 1
            if program_counter >= len(problem_input):
                break

            if problem_input[program_counter] == "noop":
                current_instruction = (problem_input[program_counter], 0)
            elif problem_input[program_counter].startswith("addx"):
                current_instruction = (problem_input[program_counter], 1)
            else:
                raise ValueError(
                    f"Unknown instruction `{problem_input[program_counter]}`"
                )
        else:
            current_instruction = (current_instruction[0], current_instruction[1] - 1)

        current_cycle += 1


def part_one(problem_input: list[str]) -> int:
    signal_index = 0
    signals = [20, 60, 100, 140, 180, 220]
    signal_values = signals.copy()

    def cycle_hook(current_cycle: int, register_value: int):
        nonlocal signal_index, signals, signal_values

        if signal_index < len(signals) and current_cycle == signals[signal_index]:
            signal_values[signal_index] = current_cycle * register_value
            signal_index += 1

    execute_program(problem_input, cycle_hook)

    return sum(signal_values)


def part_two(problem_input: list[str]) -> str:
    screen = [["."] * 40 for _ in range(6)]

    def cycle_hook(current_cycle: int, register_value: int):
        nonlocal screen

        position = current_cycle - 1
        row = int(position / 40)
        cell = position % 40
        if register_value - 1 <= cell and cell <= register_value + 1:
            screen[row][cell] = "#"

    execute_program(problem_input, cycle_hook)

    return "\n" + "\n".join("".join(row) for row in screen)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
