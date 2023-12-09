from pathlib import Path

import requests
from dotenv import dotenv_values


def get_and_cache_input(file_path_str: str) -> list[str]:
    file_path = Path(file_path_str)
    input_file_path = file_path.with_suffix(".input.txt")
    if input_file_path.exists() and input_file_path.stat().st_size > 0:
        with open(input_file_path, "r", encoding="utf-8") as file:
            return [line.rstrip() for line in file]

    year = file_path.parent.stem
    day = file_path.stem.removeprefix("day")
    assert (
        year.isnumeric() and day.isnumeric()
    ), f'Failed to parse year "{year}" and day "{day}"'

    session_token = dotenv_values(file_path.parent.with_name(".env")).get("AOC_SESSION")
    if session_token is None:
        raise ValueError("Missing session token")

    res = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": session_token},
    )
    if res.status_code != 200:
        raise ValueError(f"Failed to retrieve input for year {year}, day {day}")

    with open(input_file_path, "w+", encoding="utf-8") as file:
        file.write(res.text)
        file.seek(0)
        return [line.rstrip() for line in file]
