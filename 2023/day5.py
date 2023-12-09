from typing import Literal

from utils import get_and_cache_input


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
            mapping = None
            if line.startswith("seed-to-soil"):
                mapping = self.seedToSoil
            elif line.startswith("soil-to-fertilizer"):
                mapping = self.soilToFertilizer
            elif line.startswith("fertilizer-to-water"):
                mapping = self.fertilizerToWater
            elif line.startswith("water-to-light"):
                mapping = self.waterToLight
            elif line.startswith("light-to-temperature"):
                mapping = self.lightToTemperature
            elif line.startswith("temperature-to-humidity"):
                mapping = self.temperatureToHumidity
            elif line.startswith("humidity-to-location"):
                mapping = self.humidityToLocation

            if mapping is not None:
                line_index += 1
                line = almanac[line_index]
                while line != "":
                    dest, source, range = line.split()
                    mapping.append((int(dest), int(source), int(range)))
                    line_index += 1
                    if line_index >= len(almanac):
                        break
                    line = almanac[line_index]
                mapping.sort(key=lambda t: t[0])
            else:
                line_index += 1

    def get_distance_to_next_edge(
        self,
        type: Literal["seed"]
        | Literal["soil"]
        | Literal["fertilizer"]
        | Literal["water"]
        | Literal["light"]
        | Literal["temperature"]
        | Literal["humidity"],
        value: int,
    ) -> int:
        if type == "seed":
            mapping = self.seedToSoil
        elif type == "soil":
            mapping = self.soilToFertilizer
        elif type == "fertilizer":
            mapping = self.fertilizerToWater
        elif type == "water":
            mapping = self.waterToLight
        elif type == "light":
            mapping = self.lightToTemperature
        elif type == "temperature":
            mapping = self.temperatureToHumidity
        elif type == "humidity":
            mapping = self.humidityToLocation

        for _, range_start, range in mapping:
            if value < range_start:
                return range_start - value
            elif range_start <= value < range_start + range:
                return range_start + range - value

        return 0

    def get_location_number(self, input_seed: int) -> tuple[int, int]:
        output_soil = input_seed
        for soil, seed, range in self.seedToSoil:
            if seed <= input_seed < seed + range:
                output_soil = soil + input_seed - seed
                break
        output_fertilizer = output_soil
        for fertilizer, soil, range in self.soilToFertilizer:
            if soil <= output_soil < soil + range:
                output_fertilizer = fertilizer + output_soil - soil
                break
        output_water = output_fertilizer
        for water, fertilizer, range in self.fertilizerToWater:
            if fertilizer <= output_fertilizer < fertilizer + range:
                output_water = water + output_fertilizer - fertilizer
                break
        output_light = output_water
        for light, water, range in self.waterToLight:
            if water <= output_water < water + range:
                output_light = light + output_water - water
                break
        output_temperature = output_light
        for temperature, light, range in self.lightToTemperature:
            if light <= output_light < light + range:
                output_temperature = temperature + output_light - light
                break
        output_humidity = output_temperature
        for humidity, temperature, range in self.temperatureToHumidity:
            if temperature <= output_temperature < temperature + range:
                output_humidity = humidity + output_temperature - temperature
                break
        output_location = output_humidity
        for location, humidity, range in self.humidityToLocation:
            if humidity <= output_humidity < humidity + range:
                output_location = location + output_humidity - humidity
                break

        seeds_to_skip = min(
            self.get_distance_to_next_edge("seed", input_seed),
            self.get_distance_to_next_edge("soil", output_soil),
            self.get_distance_to_next_edge("fertilizer", output_fertilizer),
            self.get_distance_to_next_edge("water", output_water),
            self.get_distance_to_next_edge("light", output_light),
            self.get_distance_to_next_edge("temperature", output_temperature),
            self.get_distance_to_next_edge("humidity", output_humidity),
        )
        return (output_location, seeds_to_skip)


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

        input_seed = seed
        while input_seed < seed + seed_range:
            location_number, seeds_to_skip = almanac.get_location_number(input_seed)
            if min_location is None or location_number < min_location:
                min_location = location_number

            if seeds_to_skip > 0:
                input_seed += seeds_to_skip
            else:
                input_seed += 1

    assert min_location is not None
    return min_location


if __name__ == "__main__":
    problem_input = get_and_cache_input(__file__)

    almanac = Almanac(problem_input)
    print("Part One: ", part_one(problem_input, almanac))
    print("Part Two: ", part_two(problem_input, almanac))
