from reader import get_string_data

from dataclasses import dataclass
from functools import reduce
import logging
import math
import os

file = __file__.split("/")[-1].split(".")[0]
RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/{file}/{RUNTIME}.txt""")


def parse_data():
    for line in DATA:
        if "Time" in line:
            times = [
                int(time) for time in line.split(": ")[1].strip().split()
            ]
        else:
            distances = [
                int(distance) for distance in line.split(": ")[1].strip().split()
            ]
    return list(zip(times, distances))


def parse_kerning():
    for line in DATA:
        num = int("".join(filter(lambda i: i.isdigit(), line)))
        if "Time" in line:
            time = num
        else:
            distances = num
    return time, distances

def part_one():
    data = parse_data()
    scores = []
    for time, distance in data:
        logging.debug(f"Processing time: {time}, distance: {distance}")
        options = 0
        for ts in range(time):
            d = (time - ts) * ts
            if d > distance:
                options += 1
        logging.debug(f"Options: {options}")
        scores.append(options)
    return reduce(lambda x, y: x * y, scores)


def part_two():
    time, distance = parse_kerning()
    logging.debug(f"Processing time: {time}, distance: {distance}")
    options = 0
    for ts in range(time):
        d = (time - ts) * ts
        if d > distance:
            options += 1
    logging.debug(f"Options: {options}")
    return options