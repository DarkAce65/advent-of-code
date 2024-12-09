from typing import Generator, NamedTuple

from utils import get_and_cache_input


class File(NamedTuple):
    id: int
    start: int
    length: int

    def compute_checksum(self, empty_block_iterator: Generator[int, None, None]) -> int:
        checksum = 0
        blocks_left = self.length
        try:
            while blocks_left > 0:
                empty_block = next(empty_block_iterator)
                if empty_block > self.start:
                    empty_block_iterator.close()
                    raise StopIteration()
                checksum += self.id * empty_block
                blocks_left -= 1
        except StopIteration:
            checksum += self.id * int(
                (self.start + self.start + blocks_left - 1) * blocks_left / 2
            )

        return checksum


class Space(NamedTuple):
    start: int
    length: int


def make_empty_block_iterator(spaces: list[Space]) -> Generator[int, None, None]:
    for space in spaces:
        for block in range(space.length):
            yield space.start + block


def part_one(problem_input: list[str]) -> int:
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

    empty_block_iterator = make_empty_block_iterator(spaces)
    checksum = 0
    for file in files[::-1]:
        x = file.compute_checksum(empty_block_iterator)
        checksum += x

    return checksum


def part_two(problem_input: list[str]) -> int:
    return 0


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
