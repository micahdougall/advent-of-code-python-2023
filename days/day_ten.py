import json
import logging
from math import sqrt
from matplotlib.pyplot import arrow, xlim, ylim, title, show
import numpy as np
from scipy.integrate import simpson


directions = {
    "|": ["north", "south"],
    "J": ["north", "west"],
    "L": ["north", "east"],
    "7": ["south", "west"],
    "F": ["south", "east"],
    "-": ["west", "east"],
}

opp_directions = {
    "north": "south",
    "south": "north",
    "west": "east",
    "east": "west",
}

moves = {
    "north": (-1, 0),
    "south": (1, 0),
    "west": (0, -1),
    "east": (0, 1),
}


def find_start_mode(data: list[list[str]]) -> tuple[int, int]:
    """Return start mode."""
    for row_index, row in enumerate(data):
        for col_index, col in enumerate(row):
            if col == "S":
                logging.info(f"Start mode found at {row_index}, {col_index}")
                return row_index, col_index


def get_char_at(data: list[list[str]], row: int, col: int) -> str:
    """Return char at row, col."""
    if row < 0 or col < 0:
        raise IndexError(f"Index out of range: {row}, {col}")
    logging.debug(f"Char at {row}, {col} = {data[row][col]}")
    return data[row][col]


def get_next_dir(char: str, previous: str) -> str:
    """Return next direction."""
    logging.debug(f"Getting next direction for {char} from {previous}")
    logging.debug(f"Directions: {directions.get(char)}")
    return next(filter(
        lambda x: not x == previous,
        directions.get(char)
    ))


def get_next_move(row: int, col: int, direction: str) -> tuple[int, int]:
    """Return next move."""
    logging.debug(f"Getting next move from {row}, {col} in {direction} direction")
    return row + moves[direction][0], col + moves[direction][1]


def is_valid_move(start_pos: tuple[int, int], dir: str, data: list[list[str]]) -> bool:
    """Return if move is valid."""
    propsed_pos = get_next_move(*start_pos, dir)
    logging.debug(f"Proposed position: {propsed_pos}")
    try:
        next_char = get_char_at(data, *propsed_pos)
        logging.debug(f"Next char: {next_char}")
        routes = directions.get(next_char)
        logging.debug(f"Routes: {routes}")
        opp_dir = opp_directions.get(dir)
        logging.debug(f"Opposite direction: {opp_dir}")
        if opp_dir not in routes:
            logging.debug(f"Opposite direction not in routes")
            return False
        valid_move = next(filter(lambda x: not x == opp_dir, routes))
        logging.debug(f"Valid move: {valid_move}")
        return valid_move
    except:
        logging.debug(f"Invalid move from {start_pos} in {dir} direction")
        return False
        

def build_path(data: list[list[str]]) -> list[tuple[int, int]]:
    """Return path."""
    path = []
    start_pos = find_start_mode(data)
    path.append(start_pos)

    for move in moves.keys():
        if is_valid_move(start_pos, move, data):
            direction = move
            break
    next_node = get_next_move(*start_pos, direction)
    while not next_node == start_pos:
        logging.debug(f"Appending next node: {next_node}")
        path.append(next_node)
        # logging.debug(f"Path: {path}")
        logging.debug(f"Path length: {len(path)}")
        char = get_char_at(data, *next_node)
        direction = get_next_dir(char, opp_directions.get(direction))
        logging.debug(f"Next direction: {direction}")
        next_node = get_next_move(*next_node, direction)
        logging.debug(f"Next node: {next_node}")
    return path


def write_path(path: list[tuple[int, int]]) -> None:
    """Write path to file."""
    with open("res/ten/path.json", "w") as f:
        json.dump(path, f)


def inner_points(route: list[list[str]]) -> float:
    boundary_points = len(route)

    # Calculate raw area inside graph
    x = [r[0] for r in route]
    y = [r[1] for r in route]
    space_area = 0.5 * np.abs(
        np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1))
    )
    # Pick's theorem: A = i + b/2 - 1, therefore: i = A - b/2 + 1
    return int(space_area - (boundary_points / 2) + 1)
