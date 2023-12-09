import re

from utils import get_and_cache_input


def part_one(problem_input: list[str]) -> str:
    stacks = [list(reversed(stack.split(" "))) for stack in problem_input[:9]]

    for action in problem_input[9:]:
        m = re.match("move ([0-9]+) from ([0-9]+) to ([0-9]+)", action)
        if m is None:
            continue

        num = int(m.group(1))
        from_stack = int(m.group(2)) - 1
        to_stack = int(m.group(3)) - 1
        for _ in range(num):
            moved_item = stacks[from_stack].pop()
            stacks[to_stack].append(moved_item)

    top_of_stacks = ""
    for s in stacks:
        top_of_stacks += s[len(s) - 1]
    return top_of_stacks


def part_two(problem_input: list[str]) -> str:
    stacks = [list(reversed(stack.split(" "))) for stack in problem_input[:9]]

    for action in problem_input[9:]:
        m = re.match("move ([0-9]+) from ([0-9]+) to ([0-9]+)", action)
        if m is None:
            continue

        num = int(m.group(1))
        from_stack = int(m.group(2)) - 1
        to_stack = int(m.group(3)) - 1
        stacks[to_stack].extend(stacks[from_stack][-num:])
        stacks[from_stack] = stacks[from_stack][:-num]

    top_of_stacks = ""
    for s in stacks:
        top_of_stacks += s[len(s) - 1]
    return top_of_stacks


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
