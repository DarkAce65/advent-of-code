from collections import defaultdict

from utils import get_and_cache_input


def parse_input(
    problem_input: list[str],
) -> tuple[list[list[int]], dict[int, set[int]], dict[int, set[int]]]:
    forward_dependencies: dict[int, set[int]] = defaultdict(set)
    backward_dependencies: dict[int, set[int]] = defaultdict(set)

    print_orders: list[list[int]] = []
    for line in problem_input:
        if "|" in line:
            x, y = line.split("|")
            backward_dependencies[int(x)].add(int(y))
            forward_dependencies[int(y)].add(int(x))
        elif len(line) > 0:
            print_orders.append([int(v) for v in line.split(",")])

    return (print_orders, forward_dependencies, backward_dependencies)


def filter_dependencies(
    print_order: list[int], dependencies: dict[int, set[int]]
) -> dict[int, set[int]]:
    pages_to_print = set(print_order)
    filtered_dependencies: dict[int, set[int]] = defaultdict(set)
    for page in dependencies.keys():
        if page not in pages_to_print:
            continue
        for dependent in dependencies[page]:
            if dependent in pages_to_print:
                filtered_dependencies[page].add(dependent)

    return filtered_dependencies


def is_correctly_ordered(
    print_order: list[int], dependencies: dict[int, set[int]]
) -> bool:
    filtered_dependencies = filter_dependencies(print_order, dependencies)

    printed: set[int] = set()
    for page in print_order:
        for dependency in filtered_dependencies[page]:
            if dependency not in printed:
                return False
        printed.add(page)

    return True


def fix_print_order(
    print_order: list[int], dependencies: dict[int, set[int]]
) -> list[int]:
    filtered_dependencies = filter_dependencies(print_order, dependencies)

    fixed_order: list[int] = []

    for page in print_order:
        insertion_index = len(fixed_order)
        for dependency in filtered_dependencies[page]:
            index = fixed_order.index(dependency) if dependency in fixed_order else -1
            if index != -1:
                insertion_index = min(index, insertion_index)

        fixed_order.insert(insertion_index, page)

    return fixed_order


def part_one(problem_input: list[str]) -> int:
    print_orders, forward_dependencies, _ = parse_input(problem_input)

    return sum(
        (
            print_order[int(len(print_order) / 2)]
            if is_correctly_ordered(print_order, forward_dependencies)
            else 0
        )
        for print_order in print_orders
    )


def part_two(problem_input: list[str]) -> int:
    print_orders, forward_dependencies, backward_dependencies = parse_input(problem_input)

    return sum(
        (
            fix_print_order(print_order, backward_dependencies)[int(len(print_order) / 2)]
            if not is_correctly_ordered(print_order, forward_dependencies)
            else 0
        )
        for print_order in print_orders
    )


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
