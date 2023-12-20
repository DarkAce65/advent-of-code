import math
from dataclasses import dataclass
from enum import Enum

from utils import get_and_cache_input


class PulseType(Enum):
    HIGH = True
    LOW = False


Pulses = list[tuple[str, str, PulseType]]


@dataclass
class Module:
    name: str
    outputs: list[str]

    def send_pulse_to_outputs(self, pulse: PulseType) -> Pulses:
        return [(self.name, output, pulse) for output in self.outputs]

    def process_inputs(self, input: tuple[str, str, PulseType]) -> Pulses:
        raise NotImplementedError()


@dataclass
class BroadcasterModule(Module):
    def process_inputs(self, input: tuple[str, str, PulseType]) -> Pulses:
        _, to_name, pulse = input
        assert to_name == self.name
        return self.send_pulse_to_outputs(pulse)


@dataclass
class FlipFlopModule(Module):
    on: bool = False

    def process_inputs(self, input: tuple[str, str, PulseType]) -> Pulses:
        from_name, to_name, pulse = input
        assert to_name == self.name
        if pulse == PulseType.LOW:
            self.on = not self.on
            return self.send_pulse_to_outputs(
                PulseType.HIGH if self.on else PulseType.LOW
            )

        return []


@dataclass
class ConjunctionModule(Module):
    memory: dict[str, PulseType]

    def process_inputs(self, input: tuple[str, str, PulseType]) -> Pulses:
        from_name, to_name, pulse = input
        assert to_name == self.name
        self.memory[from_name] = pulse
        return self.send_pulse_to_outputs(
            PulseType.LOW
            if all(value == PulseType.HIGH for value in self.memory.values())
            else PulseType.HIGH
        )


def build_modules(problem_input: list[str]) -> dict[str, Module]:
    modules: dict[str, Module] = {}
    for line in problem_input:
        if line.startswith("broadcaster"):
            modules["broadcaster"] = BroadcasterModule(
                "broadcaster",
                [module_name.strip() for module_name in line.split("->")[1].split(",")],
            )
        elif line.startswith("%"):
            module_name, outputs = line.split("->")
            trimmed_module_name = module_name.removeprefix("%").strip()
            modules[trimmed_module_name] = FlipFlopModule(
                trimmed_module_name,
                [module_name.strip() for module_name in outputs.split(",")],
            )
        elif line.startswith("&"):
            module_name, outputs = line.split("->")
            trimmed_module_name = module_name.removeprefix("&").strip()
            output_modules = [module_name.strip() for module_name in outputs.split(",")]
            modules[trimmed_module_name] = ConjunctionModule(
                trimmed_module_name, output_modules, {}
            )

    for module in modules.values():
        for output in module.outputs:
            if output in modules:
                output_module = modules[output]
                if isinstance(output_module, ConjunctionModule):
                    output_module.memory[module.name] = PulseType.LOW

    return modules


def push_button(modules: dict[str, Module]) -> tuple[int, int]:
    low_pulses = 0
    high_pulses = 0

    pulses: Pulses = [("button", "broadcaster", PulseType.LOW)]
    while len(pulses) > 0:
        for _, _, pulse in pulses:
            if pulse == PulseType.HIGH:
                high_pulses += 1
            elif pulse == PulseType.LOW:
                low_pulses += 1
        next_pulses: Pulses = []
        for from_module, to_module, pulse in pulses:
            if to_module in modules:
                outputs = modules[to_module].process_inputs(
                    (from_module, to_module, pulse)
                )
                next_pulses.extend(outputs)
        pulses = next_pulses

    return (low_pulses, high_pulses)


def push_button_til_high(modules: dict[str, Module], module_name: str) -> int:
    num_pushes = 0

    while True:
        num_pushes += 1
        pulses: Pulses = [("button", "broadcaster", PulseType.LOW)]
        while len(pulses) > 0:
            next_pulses: Pulses = []
            for from_module, to_module, pulse in pulses:
                if from_module == module_name and pulse == PulseType.HIGH:
                    return num_pushes

                if to_module in modules:
                    outputs = modules[to_module].process_inputs(
                        (from_module, to_module, pulse)
                    )
                    next_pulses.extend(outputs)
            pulses = next_pulses


def part_one(problem_input: list[str]) -> int:
    modules = build_modules(problem_input)

    low_pulses = 0
    high_pulses = 0

    for _ in range(1000):
        low, high = push_button(modules)
        low_pulses += low
        high_pulses += high

    return low_pulses * high_pulses


def part_two(problem_input: list[str]) -> int:
    modules1 = build_modules(problem_input)
    modules2 = build_modules(problem_input)
    modules3 = build_modules(problem_input)
    modules4 = build_modules(problem_input)
    p1 = push_button_til_high(modules1, "ss")
    p2 = push_button_til_high(modules2, "fz")
    p3 = push_button_til_high(modules3, "mf")
    p4 = push_button_til_high(modules4, "fh")

    print(p1, p2, p3, p4)

    return math.lcm(p1, p2, p3, p4)


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
