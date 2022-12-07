from pathlib import Path
from typing import Any


def parse_filesystem(commands: list[str]) -> dict[str, int]:
    files: dict[str, int] = {"/": 0}
    cwd = "/"
    i = 0
    while i < len(commands):
        command = commands[i]
        if command.startswith("$ cd"):
            path = command.removeprefix("$ cd ")
            if path == "/":
                cwd = "/"
            elif path == "..":
                cwd = cwd.rsplit("/", 2)[0] + "/"
            else:
                cwd = cwd + path + "/"
            i += 1
        elif command == "$ ls":
            i += 1
            while i < len(commands):
                line = commands[i]
                if line.startswith("$"):
                    break

                if line.startswith("dir"):
                    dir = line.removeprefix("dir ")
                    files[cwd + dir + "/"] = 0
                else:
                    size, filename = line.split(" ")
                    files[cwd + filename] = int(size)
                i += 1
        else:
            raise ValueError("Unrecognized command '" + command + "'")

    for path in files.keys():
        if path.endswith("/"):
            files[path] = sum(files[p] for p in files.keys() if p.startswith(path))

    return files


def part_one(problem_input: list[str]) -> int:
    files = parse_filesystem(problem_input)

    return sum(
        files[path]
        for path in files.keys()
        if path.endswith("/") and files[path] <= 100000
    )


def part_two(problem_input: list[str]) -> int:
    files = parse_filesystem(problem_input)

    unused_space = 70000000 - files["/"]
    delete_at_least = 30000000 - unused_space

    smallest_dir_size_to_delete = files["/"]
    for path in files.keys():
        if (
            path.endswith("/")
            and smallest_dir_size_to_delete > files[path]
            and files[path] >= delete_at_least
        ):
            smallest_dir_size_to_delete = files[path]

    return smallest_dir_size_to_delete


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
