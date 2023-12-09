import math
from collections import deque
from typing import Optional, Union

from utils import get_and_cache_input

CLOSING_CHUNK_DELIMITERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

AUTOCOMPLETE_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
SYNTAX_ERROR_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


class MismatchedChunkDelimiter(Exception):
    error_character: str

    def __init__(self, *args: object, error_character: str) -> None:
        super().__init__(*args)
        self.error_character = error_character


def parse_chunks(line: str) -> Union[str, deque[str]]:
    open_chunks: deque[str] = deque()

    for c in line:
        if c == ")":
            if len(open_chunks) == 0 or open_chunks.pop() != "(":
                raise MismatchedChunkDelimiter(error_character=c)
        elif c == "]":
            if len(open_chunks) == 0 or open_chunks.pop() != "[":
                raise MismatchedChunkDelimiter(error_character=c)
        elif c == "}":
            if len(open_chunks) == 0 or open_chunks.pop() != "{":
                raise MismatchedChunkDelimiter(error_character=c)
        elif c == ">":
            if len(open_chunks) == 0 or open_chunks.pop() != "<":
                raise MismatchedChunkDelimiter(error_character=c)
        else:
            open_chunks.append(c)

    return open_chunks


def get_first_illegal_character(line: str) -> Optional[str]:
    try:
        parse_chunks(line)
    except MismatchedChunkDelimiter as error:
        return error.error_character

    return None


def part_one(problem_input: list[str]) -> int:
    syntax_error_score = 0

    for line in problem_input:
        illegal_character = get_first_illegal_character(line)
        if illegal_character is not None:
            syntax_error_score += SYNTAX_ERROR_SCORES[illegal_character]

    return syntax_error_score


def part_two(problem_input: list[str]):
    autocomplete_scores = []

    for line in problem_input:
        try:
            open_chunks = parse_chunks(line)
        except MismatchedChunkDelimiter:
            continue

        autocomplete_score = 0
        for open_delimiter in list(open_chunks)[::-1]:
            autocomplete_score = (
                autocomplete_score * 5
                + AUTOCOMPLETE_SCORES[CLOSING_CHUNK_DELIMITERS[open_delimiter]]
            )

        autocomplete_scores.append(autocomplete_score)

    return sorted(autocomplete_scores)[math.floor(len(autocomplete_scores) / 2)]


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    print("Part One: ", part_one(problem_input))
    print("Part Two: ", part_two(problem_input))
