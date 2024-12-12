from __future__ import annotations

from typing import Callable, NamedTuple

from utils import get_and_cache_input


class File(NamedTuple):
    id: int
    start: int
    length: int

    def compute_checksum(
        self, request_free_space: Callable[[int, int], list[int] | None]
    ) -> int:
        checksum = 0
        blocks_left = self.length
        blocks = request_free_space(self.start, blocks_left)
        if blocks is not None:
            for block in blocks:
                checksum += self.id * block
                blocks_left -= 1

        if blocks_left > 0:
            checksum += self.id * int(
                (self.start + self.start + blocks_left - 1) * blocks_left / 2
            )

        return checksum


class Space(NamedTuple):
    start: int
    length: int


def parse_files_and_spaces(problem_input: list[str]) -> tuple[list[File], list[Space]]:
    is_file = True

    block_index = 0
    files: list[File] = []
    spaces: list[Space] = []
    for c in problem_input[0]:
        value = int(c)
        if is_file:
            files.append(File(len(files), block_index, value))
        else:
            spaces.append(Space(block_index, value))
        block_index += value
        is_file = not is_file

    return (files, spaces)


class LinkedBlocks:
    start: int
    length: int

    prev: LinkedBlocks | None = None
    next: LinkedBlocks | None = None

    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length

    def get_next_free_block(start: LinkedBlocks, length: int) -> LinkedSpace | None:
        current: LinkedBlocks | None = start
        while current is not None:
            if isinstance(current, LinkedSpace) and current.length >= length:
                return current
            current = current.next

        return None


class LinkedSpace(LinkedBlocks):
    def compact(self) -> None:
        if isinstance(self.prev, LinkedSpace):
            self.prev.compact()
        else:
            while isinstance(self.next, LinkedSpace):
                self.length += self.next.length
                self.next = self.next.next
            if self.next is not None:
                self.next.prev = self

    def move_file_here(self, file: LinkedFile) -> None:
        file_space = LinkedSpace(file.start, file.length)
        if file.next is not None:
            file_space.next = file.next
            file.next.prev = file_space
        if file.prev is not None:
            file_space.prev = file.prev
            file.prev.next = file_space

        file.start = self.start
        if self.prev is not None:
            self.prev.next = file
            file.prev = self.prev

        remaining_space = self.length - file.length
        if remaining_space > 0:
            self.start += file.length
            self.length = remaining_space

            self.prev = file
            file.next = self
        else:
            if self.next is not None:
                self.next.prev = file
                file.next = self.next

        file_space.compact()


class LinkedFile(LinkedBlocks):
    id: int

    def __init__(self, id: int, start: int, length: int):
        super().__init__(start, length)
        self.id = id

    def compute_checksum(self) -> int:
        return self.id * int(
            (self.start + self.start + self.length - 1) * self.length / 2
        )


def parse_file_list(problem_input: list[str]) -> tuple[LinkedBlocks, LinkedBlocks]:
    is_file = False

    num_files = 0
    block_index = 0
    head: LinkedBlocks | None = None
    tail: LinkedBlocks | None = None
    for c in problem_input[0]:
        is_file = not is_file
        value = int(c)
        if value == 0:
            continue

        blocks: LinkedBlocks | None = None
        if is_file:
            blocks = LinkedFile(num_files, block_index, value)
            num_files += 1
        else:
            blocks = LinkedSpace(block_index, value)

        block_index += value

        assert blocks is not None
        if tail is not None:
            tail.next = blocks
            blocks.prev = tail
        if head is None:
            head = blocks
        tail = blocks

    assert head is not None
    assert tail is not None
    return (head, tail)


def make_request_free_space(
    spaces: list[Space],
) -> Callable[
    [int, int],
    list[int] | None,
]:
    space_index = 0
    space_block_offset = 0

    def request_free_space(start_block: int, num_blocks: int) -> list[int] | None:
        nonlocal space_index, space_block_offset

        if (
            space_index >= len(spaces)
            or spaces[space_index].start + space_block_offset > start_block
        ):
            return None

        free_blocks: list[int] = []

        free_blocks = []
        while space_index < len(spaces) and len(free_blocks) < num_blocks:
            if spaces[space_index].start + space_block_offset > start_block:
                break
            free_blocks.append(spaces[space_index].start + space_block_offset)
            space_block_offset += 1
            if spaces[space_index].length <= space_block_offset:
                space_index += 1
                space_block_offset = 0
        return free_blocks

    return request_free_space


def part_one(problem_input: list[str]) -> int:
    files, spaces = parse_files_and_spaces(problem_input)

    request_free_space = make_request_free_space(spaces)
    checksum = 0
    for file in files[::-1]:
        checksum += file.compute_checksum(request_free_space)

    return checksum


def part_two(problem_input: list[str]) -> int:
    head, tail = parse_file_list(problem_input)
    files: list[LinkedFile] = []
    f: LinkedBlocks | None = tail
    while f is not None:
        if isinstance(f, LinkedFile):
            files.append(f)
        f = f.prev

    checksum = 0
    current: LinkedBlocks | None = tail
    while current is not None and not isinstance(current, LinkedFile):
        current = current.prev
    for file in files:
        space = LinkedBlocks.get_next_free_block(head, file.length)
        if space is not None and space.start < file.start:
            space.move_file_here(file)

        checksum += file.compute_checksum()

    return checksum


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
