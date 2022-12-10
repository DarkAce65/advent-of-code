from pathlib import Path


def part_one(problem_input: list[str]) -> int:
    signal_index = 0
    signals = [20, 60, 100, 140, 180, 220]
    signal_values = signals.copy()

    current_cycle = 1
    register_value = 1
    for instr in problem_input:
        if current_cycle == signals[signal_index]:
            signal_values[signal_index] = signals[signal_index] * register_value
            signal_index += 1

        if signal_index >= len(signals):
            break

        if instr == "noop":
            current_cycle += 1
        elif instr.startswith("addx"):
            if current_cycle + 1 == signals[signal_index]:
                signal_values[signal_index] = signals[signal_index] * register_value
                signal_index += 1

            inc = int(instr.split(" ")[1])
            register_value += inc
            current_cycle += 2

        if signal_index >= len(signals):
            break

    if signal_index < len(signals) and current_cycle == signals[signal_index]:
        signal_values[signal_index] = signals[signal_index] * register_value
        signal_index += 1

    return sum(signal_values)


def part_two(problem_input: list[str]):
    screen = ["." * 40 for _ in range(6)]

    current_cycle = 0
    register_value = 1
    for instr in problem_input:
        row = int(current_cycle / 40)
        cell = current_cycle % 40
        if register_value - 1 <= cell and cell <= register_value + 1:
            screen[row] = screen[row][:cell] + "#" + screen[row][cell + 1 :]

        if instr == "noop":
            current_cycle += 1
        elif instr.startswith("addx"):
            current_cycle += 1
            row = int(current_cycle / 40)
            cell = current_cycle % 40
            if register_value - 1 <= cell and cell <= register_value + 1:
                screen[row] = screen[row][:cell] + "#" + screen[row][cell + 1 :]
            inc = int(instr.split(" ")[1])
            register_value += inc
            current_cycle += 1

    row = int(current_cycle / 40)
    cell = current_cycle % 40
    if register_value - 1 <= cell and cell <= register_value + 1:
        screen[row] = screen[row][:cell] + "#" + screen[row][cell + 1 :]

    for line in screen:
        print(line)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
