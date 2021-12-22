from pathlib import Path
from typing import Optional


class InfiniteImage:
    lit_pixels: set[tuple[int, int]]
    is_background_lit: bool
    row_bounds: tuple[int, int]
    col_bounds: tuple[int, int]

    def __init__(self, lit_pixels: Optional[set[tuple[int, int]]] = None) -> None:
        self.lit_pixels = lit_pixels or set()
        self.is_background_lit = False
        self.compute_bounds()

    def load_image(self, lit_pixels: set[tuple[int, int]]) -> None:
        self.lit_pixels = lit_pixels.copy()

    def is_pixel_lit(self, row: int, col: int) -> bool:
        if (
            row < self.row_bounds[0]
            or self.row_bounds[1] < row
            or col < self.col_bounds[0]
            or self.col_bounds[1] < col
        ):
            return self.is_background_lit

        return (row, col) in self.lit_pixels

    def light_pixel(self, row: int, col: int) -> None:
        self.lit_pixels.add((row, col))

    def compute_bounds(self) -> None:
        if len(self.lit_pixels) == 0:
            self.row_bounds = (0, 0)
            self.col_bounds = (0, 0)
        else:
            self.row_bounds = (
                min(row for (row, _) in self.lit_pixels),
                max(row for (row, _) in self.lit_pixels),
            )
            self.col_bounds = (
                min(col for (_, col) in self.lit_pixels),
                max(col for (_, col) in self.lit_pixels),
            )

    def paint(self) -> None:
        (min_row, max_row) = self.row_bounds
        (min_col, max_col) = self.col_bounds

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if (row, col) in self.lit_pixels:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def enhance_image(
    image_enhancement_algorithm: str, image: InfiniteImage
) -> InfiniteImage:
    enhanced_image = InfiniteImage()

    (min_row, max_row) = image.row_bounds
    (min_col, max_col) = image.col_bounds

    for row in range(min_row - 1, max_row + 2):
        for col in range(min_col - 1, max_col + 2):
            enhancement_index = ""
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if image.is_pixel_lit(r, c):
                        enhancement_index += "1"
                    else:
                        enhancement_index += "0"

            if image_enhancement_algorithm[int(enhancement_index, 2)] == "#":
                enhanced_image.light_pixel(row, col)

    if image.is_background_lit and image_enhancement_algorithm[511] == ".":
        enhanced_image.is_background_lit = False
    elif not image.is_background_lit and image_enhancement_algorithm[0] == "#":
        enhanced_image.is_background_lit = True

    enhanced_image.compute_bounds()

    return enhanced_image


def part_one(image_enhancement_algorithm: str, input_image: list[str]) -> int:
    lit_pixels: set[tuple[int, int]] = set()
    for row in range(len(input_image)):
        for col in range(len(input_image[row])):
            if input_image[row][col] == "#":
                lit_pixels.add((row, col))

    image = InfiniteImage(lit_pixels)
    image = enhance_image(image_enhancement_algorithm, image)
    image = enhance_image(image_enhancement_algorithm, image)

    return len(image.lit_pixels)


def part_two(image_enhancement_algorithm: str, input_image: list[str]) -> int:
    lit_pixels: set[tuple[int, int]] = set()
    for row in range(len(input_image)):
        for col in range(len(input_image[row])):
            if input_image[row][col] == "#":
                lit_pixels.add((row, col))

    image = InfiniteImage(lit_pixels)
    for _ in range(50):
        image = enhance_image(image_enhancement_algorithm, image)

    return len(image.lit_pixels)


if __name__ == "__main__":
    with open(Path(__file__).stem + ".input.txt", "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    image_enhancement_algorithm = problem_input[0]
    input_image = list(filter(None, problem_input[1:]))

    print("Part One: ", part_one(image_enhancement_algorithm, input_image))
    print("Part Two: ", part_two(image_enhancement_algorithm, input_image))
