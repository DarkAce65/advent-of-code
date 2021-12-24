from pathlib import Path
from typing import Optional


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
                self.save_value(a_raw, int(a / b))
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


def part_one(problem_input: list[str]) -> int:
    alu = ALU()
    program_vars = alu.run_program(problem_input, list(map(int, "13579246899999")))
    print(program_vars)

    return 0


def part_two(problem_input: list[str]) -> int:
    pass


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
