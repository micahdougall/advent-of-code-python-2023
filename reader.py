import logging
import re


def get_numeric_data(filename: str) -> list[int]:
    """Return list of strings from file."""
    with open(filename, "r") as f:
        return [[int(i) for i in line.strip().split(" ")] for line in f.readlines()]


def get_string_data(filename: str) -> list[str]:
    """Return list of strings from file."""
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_cube_game_data(filename: str) -> list[dict]:
    """Extract cube game data from file."""
    lines = get_string_data(filename)
    data = []
    for line in lines:
        game, cube_data = line.split(": ")
        game_id = re.search(r"\AGame ([0-9]+)", game).group(1)

        game_data = {}

        for turns in cube_data.split("; "):
            cubes = turns.split(", ")
            for cube in cubes:
                cube_count, cube_color = cube.split(" ")
                logging.debug(f"{cube_color} cube has count of {cube_count}")

                if (
                    cube_color not in game_data.keys() 
                    or int(cube_count) > game_data.get(cube_color)
                ):
                    game_data[cube_color] = int(cube_count)

        data.append({"id": game_id, "cubes": game_data})
    return data


