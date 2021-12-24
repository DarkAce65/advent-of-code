from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Optional


class VariableState:
    value: Optional[int]

    def __init__(self, value: Optional[int] = None) -> None:
        self.value = value

    def is_constant(self) -> bool:
        return self.value is not None

    def __add__(self, other: VariableState) -> VariableState:
        if self.value is None or other.value is None:
            return VariableState()
        return VariableState(self.value + other.value)

    def __mul__(self, other: VariableState) -> VariableState:
        if self.value == 0 or other.value == 0:
            return VariableState(0)
        elif self.value is None or other.value is None:
            return VariableState()
        return VariableState(self.value * other.value)

    def __floordiv__(self, other: VariableState) -> VariableState:
        if self.value == 0:
            return VariableState(0)
        elif self.value is None or other.value is None:
            return VariableState()
        return VariableState(self.value // other.value)

    def __mod__(self, other: VariableState) -> VariableState:
        if self.value == 0:
            return VariableState(0)
        elif self.value is None or other.value is None:
            return VariableState()
        return VariableState(self.value % other.value)

    def eql(self, other: VariableState) -> VariableState:
        if self.value is None or other.value is None:
            return VariableState()
        return VariableState(int(self.value == other.value))


class VariableStates:
    w_state: VariableState = VariableState(0)
    x_state: VariableState = VariableState(0)
    y_state: VariableState = VariableState(0)
    z_state: VariableState = VariableState(0)

    def get_state(self, var: str) -> VariableState:
        if var == "w":
            return self.w_state
        elif var == "x":
            return self.x_state
        elif var == "y":
            return self.y_state
        elif var == "z":
            return self.z_state

        raise ValueError(f"Invalid variable: {var}")

    def set_state(self, var: str, state: VariableState) -> None:
        if var == "w":
            self.w_state = state
        elif var == "x":
            self.x_state = state
        elif var == "y":
            self.y_state = state
        elif var == "z":
            self.z_state = state
        else:
            raise ValueError(f"Invalid variable: {var}")


class ALU:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    _input_values: list[int]
    _input_index: int

    def reset(self) -> None:
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

        self._input_values = []
        self._input_index = 0

    def get_value(self, var: str) -> int:
        if var == "w":
            return self.w
        elif var == "x":
            return self.x
        elif var == "y":
            return self.y
        elif var == "z":
            return self.z

        raise ValueError(f"Invalid variable: {var}")

    def save_value(self, var: str, value: int) -> None:
        if var == "w":
            self.w = value
        elif var == "x":
            self.x = value
        elif var == "y":
            self.y = value
        elif var == "z":
            self.z = value
        else:
            raise ValueError(f"Invalid variable: {var}")

    def _execute_instruction(self, instruction: str) -> None:
        [operation, *tokens] = instruction.split()
        a_raw = tokens[0]

        if operation == "inp":
            if self._input_index >= len(self._input_values):
                raise ValueError(f"Expected input for instruction: {instruction}")
            self.save_value(a_raw, self._input_values[self._input_index])
            self._input_index += 1
        elif operation in ["add", "mul", "div", "mod", "eql"]:
            b_raw = tokens[1]
            a = self.get_value(a_raw)
            if b_raw.isalpha():
                b = self.get_value(b_raw)
            else:
                b = int(b_raw)

            if operation == "add":
                self.save_value(a_raw, a + b)
            elif operation == "mul":
                self.save_value(a_raw, a * b)
            elif operation == "div":
                self.save_value(a_raw, a // b)
            elif operation == "mod":
                self.save_value(a_raw, a % b)
            elif operation == "eql":
                self.save_value(a_raw, int(a == b))
        else:
            raise ValueError(f"Unrecognized operation: {operation}")

    def run_program(
        self, program: list[str], input_values: list[int] = []
    ) -> tuple[int, int, int, int]:
        self.reset()

        self._input_values = input_values
        for instruction in program:
            self._execute_instruction(instruction)

        return (self.w, self.x, self.y, self.z)

    @staticmethod
    def _remove_overwritten_instructions(
        optimized_program: deque[tuple[str, str, Optional[str]]], var: str
    ) -> None:
        index = len(optimized_program) - 1
        while index >= 0:
            (instruction, a, b) = optimized_program[index]
            if not instruction.startswith("inp"):
                if a == var:
                    del optimized_program[index]
                elif b == var:
                    break
            index -= 1

    @staticmethod
    def optimize_program(program: list[str]) -> list[str]:
        optimized_program: deque[tuple[str, str, Optional[str]]] = deque()

        variable_states = VariableStates()

        for instruction in program:
            [operation, *tokens] = instruction.split()
            a_raw = tokens[0]
            a_state = variable_states.get_state(a_raw)

            if operation == "inp":
                ALU._remove_overwritten_instructions(optimized_program, a_raw)
                variable_states.set_state(a_raw, VariableState())
                optimized_program.append((instruction, a_raw, None))
            elif operation in ["add", "mul", "div", "mod", "eql"]:
                b_raw = tokens[1]
                if b_raw.isalpha():
                    b_state = variable_states.get_state(b_raw)
                else:
                    b_state = VariableState(int(b_raw))

                def insert_set_operation(combined_state: VariableState) -> None:
                    if combined_state.value != 0:
                        ALU._remove_overwritten_instructions(optimized_program, a_raw)
                        if not a_state.is_constant() or a_state.value != 0:
                            optimized_program.append((f"mul {a_raw} 0", a_raw, None))
                        optimized_program.append(
                            (f"add {a_raw} {combined_state.value}", a_raw, None)
                        )

                if operation == "add":
                    combined_state = a_state + b_state
                    variable_states.set_state(a_raw, combined_state)
                    if combined_state.is_constant():
                        insert_set_operation(combined_state)
                    else:
                        optimized_program.append(
                            (instruction, a_raw, b_raw if b_raw.isalpha() else None)
                        )
                elif operation == "mul":
                    combined_state = a_state * b_state
                    variable_states.set_state(a_raw, combined_state)
                    if combined_state.is_constant():
                        insert_set_operation(combined_state)
                    else:
                        optimized_program.append(
                            (instruction, a_raw, b_raw if b_raw.isalpha() else None)
                        )
                elif operation == "div":
                    combined_state = a_state // b_state
                    variable_states.set_state(a_raw, combined_state)
                    if combined_state.is_constant():
                        insert_set_operation(combined_state)
                    else:
                        optimized_program.append(
                            (instruction, a_raw, b_raw if b_raw.isalpha() else None)
                        )
                elif operation == "mod":
                    combined_state = a_state % b_state
                    variable_states.set_state(a_raw, combined_state)
                    if combined_state.is_constant():
                        insert_set_operation(combined_state)
                    else:
                        optimized_program.append(
                            (instruction, a_raw, b_raw if b_raw.isalpha() else None)
                        )
                elif operation == "eql":
                    combined_state = a_state.eql(b_state)
                    variable_states.set_state(a_raw, combined_state)
                    if combined_state.is_constant():
                        insert_set_operation(combined_state)
                    else:
                        optimized_program.append(
                            (instruction, a_raw, b_raw if b_raw.isalpha() else None)
                        )

        return list(map(lambda instr: instr[0], optimized_program))


def part_one(problem_input: list[str]) -> int:
    alu = ALU()
    optimized_program = alu.optimize_program(problem_input)

    for model_number in range(99_999_999_999_999, 11_111_111_111_111, -1):
        if "0" in str(model_number):
            continue

        (_, _, _, z) = alu.run_program(
            optimized_program, list(map(int, str(model_number)))
        )
        if z == 0:
            return model_number

    raise ValueError("No valid model number found")


def part_two(problem_input: list[str]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
