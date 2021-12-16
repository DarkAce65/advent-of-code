from pathlib import Path


class BingoBoard:
    grid: list[list[int]]
    marked: list[list[bool]]
    won: bool

    def __init__(self, number_rows: list[str]) -> None:
        self.grid = []
        self.marked = []
        for number_row in number_rows:
            grid_row = list(map(int, number_row.split()))
            self.grid.append(grid_row)
            self.marked.append([False] * len(grid_row))

        self.won = False

    def _mark(self, row: int, col: int) -> bool:
        self.marked[row][col] = True
        self.won = all(self.marked[row]) or all(
            marked_row[col] for marked_row in self.marked
        )

        return self.won

    def mark(self, number: int) -> bool:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == number:
                    return self._mark(row, col)

        return self.won

    def get_score(self) -> int:
        score = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if not self.marked[row][col]:
                    score += self.grid[row][col]

        return score

    def reset(self) -> None:
        for row in range(len(self.marked)):
            for col in range(len(self.marked[row])):
                self.marked[row][col] = False
        self.won = False


def part_one(numbers_to_call: list[int], boards: list[BingoBoard]) -> int:
    for number in numbers_to_call:
        for board in boards:
            if board.mark(number):
                return number * board.get_score()

    raise ValueError("No board won!")


def part_two(numbers_to_call: list[int], boards: list[BingoBoard]) -> int:
    last_board_to_win = None
    boards_left = boards
    for number in numbers_to_call:
        for board in boards_left:
            if board.mark(number):
                last_board_to_win = board

        boards_left = list(filter(lambda b: not b.won, boards))
        if len(boards_left) == 0 and last_board_to_win is not None:
            return number * last_board_to_win.get_score()

    if last_board_to_win is not None:
        return number * last_board_to_win.get_score()

    raise ValueError("No board won!")


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    numbers_to_call = list(map(int, problem_input[0].split(",")))

    boards: list[BingoBoard] = []
    board_input: list[str] = []
    for input_row in problem_input[1:]:
        if not input_row:
            continue

        board_input.append(input_row)
        if len(board_input) == 5:
            boards.append(BingoBoard(board_input))
            board_input = []

    print("Part One: ", part_one(numbers_to_call, boards))
    for board in boards:
        board.reset()
    print("Part Two: ", part_two(numbers_to_call, boards))
