from reader import get_string_data
from writer import write_json

from dataclasses import dataclass
import logging
import math
import os

file = __file__.split("/")[-1].split(".")[0]
RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/{file}/{RUNTIME}.txt""")


def parse_data():
    soil_data = {}
    key = ""
    for line in DATA:
        if line == "":
            logging.debug("Skipping empty line")
            continue
        elif "seeds:" in line:
            numbers = line.split(": ")[1].strip().split()
            soil_data["seeds"] = [int(i) for i in numbers]
            soil_data["seeds-group"] = {
                "seeds": [int(s) for i, s in enumerate(numbers) if i % 2 == 0],
                "range": [int(s) for i, s in enumerate(numbers) if i % 2 == 1] 
            }
        elif "map:" in line:
            key = line.split(" map:")[0]
            soil_data[key] = []
        else:
            logging.debug(f"Processing line: {line}")
            dest, source, count = line.strip().split()
            soil_data[key].append({
                "source": int(source),
                "dest": int(dest),
                "count": int(count)
            })
    return soil_data


def get_dest(list: dict, num: str):
    for map in list:
        source = map["source"]
        count = map["count"]
        if source <= num < source +count:
            return map["dest"] + (num - source)
    return num


def get_source(list: dict, num: str):
    for map in list:
        dest = map["dest"]
        count = map["count"]
        if dest <= num < dest +count:
            return map["source"] + (num - dest)
    return num


def part_one():
    soil_data = parse_data()
    write_json(file, soil_data)
    
    locations = []

    for seed in soil_data["seeds"]:
        soil = get_dest(soil_data["seed-to-soil"], seed)
        fertilizer = get_dest(soil_data["soil-to-fertilizer"], soil)
        water = get_dest(soil_data["fertilizer-to-water"], fertilizer)
        light = get_dest(soil_data["water-to-light"], water)
        temperature = get_dest(soil_data["light-to-temperature"], light)
        humidity = get_dest(soil_data["temperature-to-humidity"], temperature)
        locations.append(
            get_dest(soil_data["humidity-to-location"], humidity)
        )
    return min(locations, key=lambda x: int(x))

def part_two():
    soil_data = parse_data()
    write_json(file, soil_data)
    
    for map in sorted(soil_data["humidity-to-location"], key=lambda x: x["dest"]):
        logging.debug(f"Processing map: {map}")
        humidity = map["source"]
        temperature = get_source(soil_data["temperature-to-humidity"], humidity)
        light = get_source(soil_data["light-to-temperature"], temperature)
        water = get_source(soil_data["water-to-light"], light)
        fertilizer = get_source(soil_data["fertilizer-to-water"], water)
        soil = get_source(soil_data["soil-to-fertilizer"], fertilizer)
        seed = get_source(soil_data["seed-to-soil"], soil)
        logging.debug(f"Seed: {seed}")

        groups = soil_data["seeds-group"]
        seeds = groups["seeds"]
        ranges = groups["range"]
        for i, s in enumerate(seeds):
            logging.debug(f"Checking seed: {seed} in range: {s} - {s + ranges[i]}")
            if seed in range(s, s + ranges[i]):
                return seed


