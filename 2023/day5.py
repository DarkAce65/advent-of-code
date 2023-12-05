import math
from pathlib import Path


class Almanac:
    seedToSoil: list[tuple[int, int, int]]
    soilToFertilizer: list[tuple[int, int, int]]
    fertilizerToWater: list[tuple[int, int, int]]
    waterToLight: list[tuple[int, int, int]]
    lightToTemperature: list[tuple[int, int, int]]
    temperatureToHumidity: list[tuple[int, int, int]]
    humidityToLocation: list[tuple[int, int, int]]

    def __init__(self, almanac: list[str]) -> None:
        self.seedToSoil = []
        self.soilToFertilizer = []
        self.fertilizerToWater = []
        self.waterToLight = []
        self.lightToTemperature = []
        self.temperatureToHumidity = []
        self.humidityToLocation = []

        line_index = 0
        while line_index < len(almanac):
            line = almanac[line_index]
            list = None
            if line.startswith("seed-to-soil"):
                list = self.seedToSoil
            elif line.startswith("soil-to-fertilizer"):
                list = self.soilToFertilizer
            elif line.startswith("fertilizer-to-water"):
                list = self.fertilizerToWater
            elif line.startswith("water-to-light"):
                list = self.waterToLight
            elif line.startswith("light-to-temperature"):
                list = self.lightToTemperature
            elif line.startswith("temperature-to-humidity"):
                list = self.temperatureToHumidity
            elif line.startswith("humidity-to-location"):
                list = self.humidityToLocation

            if list is not None:
                line_index += 1
                line = almanac[line_index]
                while line != "":
                    dest, source, range = line.split()
                    list.append((int(dest), int(source), int(range)))
                    line_index += 1
                    if line_index >= len(almanac):
                        break
                    line = almanac[line_index]
                list.sort(key=lambda t: t[0])
            else:
                line_index += 1

    def get_location_number(self, input_seed: int) -> tuple[int, int]:
        can_skip = 0

        output_soil = input_seed
        for soil, seed, range in self.seedToSoil:
            if seed <= input_seed < seed + range:
                output_soil = soil + input_seed - seed
                can_skip = seed + range - input_seed
                break
        output_fertilizer = output_soil
        for fertilizer, soil, range in self.soilToFertilizer:
            if soil <= output_soil < soil + range:
                output_fertilizer = fertilizer + output_soil - soil
                can_skip = min(can_skip, soil + range - output_soil)
                break
        output_water = output_fertilizer
        for water, fertilizer, range in self.fertilizerToWater:
            if fertilizer <= output_fertilizer < fertilizer + range:
                output_water = water + output_fertilizer - fertilizer
                can_skip = min(can_skip, fertilizer + range - output_fertilizer)
                break
        output_light = output_water
        for light, water, range in self.waterToLight:
            if water <= output_water < water + range:
                output_light = light + output_water - water
                can_skip = min(can_skip, water + range - output_water)
                break
        output_temperature = output_light
        for temperature, light, range in self.lightToTemperature:
            if light <= output_light < light + range:
                output_temperature = temperature + output_light - light
                can_skip = min(can_skip, light + range - output_light)
                break
        output_humidity = output_temperature
        for humidity, temperature, range in self.temperatureToHumidity:
            if temperature <= output_temperature < temperature + range:
                output_humidity = humidity + output_temperature - temperature
                can_skip = min(can_skip, temperature + range - output_temperature)
                break
        output_location = output_humidity
        for location, humidity, range in self.humidityToLocation:
            if humidity <= output_humidity < humidity + range:
                output_location = location + output_humidity - humidity
                can_skip = min(can_skip, humidity + range - output_humidity)
                break

        return (output_location, can_skip)


def part_one(problem_input: list[str], almanac: Almanac) -> int:
    return min(
        almanac.get_location_number(int(input_seed))[0]
        for input_seed in problem_input[0].strip("seeds: ").split()
    )


def part_two(problem_input: list[str], almanac: Almanac) -> int:
    min_location = None
    seeds = [int(input_seed) for input_seed in problem_input[0].strip("seeds: ").split()]

    for index in range(0, len(seeds), 2):
        seed = seeds[index]
        seed_range = seeds[index + 1]
        print("new seed range", seed, seed_range)

        input_seed = seed
        while input_seed < seed + seed_range:
            location_number, can_skip = almanac.get_location_number(input_seed)
            if min_location is None or location_number < min_location:
                min_location = location_number
                print(input_seed, min_location)

            if can_skip > 0:
                input_seed += can_skip
            else:
                input_seed += 1

    assert min_location is not None
    return min_location


if __name__ == "__main__":
    with open(Path(__file__).with_suffix(".input.txt"), "r", encoding="utf-8") as file:
        problem_input = [line.rstrip() for line in file]

    almanac = Almanac(problem_input)
    print("Part One: ", part_one(problem_input, almanac))
    print("Part Two: ", part_two(problem_input, almanac))
