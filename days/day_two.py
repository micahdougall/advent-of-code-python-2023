from reader import get_cube_game_data

import logging
import math
import os

RUNTIME = os.environ.get("RUNTIME")
DATA = get_cube_game_data(f"""res/two/{RUNTIME}.txt""")


def part_one() -> list[dict]:
    """Return list of valid games."""
    logging.debug(f"game_data: {DATA}")

    max_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    valid_games = filter(
        lambda game: all(
            [
                cube_count <= max_cubes.get(cube)
                for cube, cube_count in game.get("cubes").items()
            ]
        ),
        DATA,
    )
    return sum([int(game.get("id")) for game in valid_games])


def part_two() -> list[dict]:
    """Return list of valid games."""
    logging.debug(f"game_data: {DATA}")

    return sum(
        [
            math.prod(game.get("cubes").values())
            for game in DATA
        ]
    )