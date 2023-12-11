from reader import get_string_data

from dataclasses import dataclass
from functools import reduce, total_ordering
import logging
import operator
import os

RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/eleven/{RUNTIME}.txt""")


@total_ordering
@dataclass(eq=True, frozen=False)
class Galaxy:
    x: int
    y: int

    def shift_right(self, amount: int = 1):
        self.x += amount

    def shift_down(self, amount: int = 1):
        self.y += amount
    
    # def __ne__(self, __value: object) -> bool:
        # return not self.__eq__(__value)
    
    def __lt__(self, other) -> bool:
        return self.x < other.x or (
            self.x == other.x and self.y < other.y
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Galaxy({self.x}, {self.y})"


def parse_galaxies(expansion: int = 1):
    logging.info(f"Parsing galaxies...expansion set to {expansion}.")
    galaxies = set()
    x_set = set()
    y_set = set()
    for y, line in enumerate(DATA):
        for x, char in enumerate(line):
            if char == "#":
                logging.debug(f"Found galaxy at ({x}, {y})")
                galaxies.add(Galaxy(x, y))
                x_set.add(x)
                y_set.add(y)
    
    missing_x = sorted(set(range(len(DATA[0]))) - x_set)
    missing_y = sorted(set(range(len(DATA))) - y_set)
    logging.info(f"Missing columns: {missing_x}")
    logging.info(f"Missing rows: {missing_y}")

    for i, x in enumerate(missing_x):
        logging.debug(f"Found empty column at {x + (i * expansion)}")
        moving = filter(
            lambda galaxy: galaxy.x > x + (i * expansion),
            galaxies
        )
        col_count = 0
        for galaxy in moving:
            col_count += 1
            logging.debug(f"Shifting {galaxy} right.")
            galaxy.shift_right(amount=expansion)
        logging.info(
            f"Shifted {col_count} galaxies right from column {x + (i * expansion)}"
        )

    for i, y in enumerate(missing_y):
        logging.debug(f"Found empty row at {y + (i * expansion)}")
        moving = filter(
            lambda galaxy: galaxy.y > y + (i * expansion),
            galaxies
        )
        row_count = 0
        for galaxy in moving:
            row_count += 1
            logging.debug(f"Shifting {galaxy} down.")
            galaxy.shift_down(amount=expansion)
        logging.debug(
            f"Shifted {row_count} galaxies down from row {y + (i * expansion)}"
        )
    logging.info(f"Found {len(galaxies)} galaxies.")
    return galaxies


def make_pairs(galaxies: list[Galaxy]) -> set[tuple[Galaxy, Galaxy]]:
    pairs = set()
    for galaxy in galaxies:
        for other_galaxy in galaxies:
            if galaxy == other_galaxy:
                continue
            pair = tuple(sorted([galaxy, other_galaxy]))
            pairs.add(pair)
    logging.info(f"Found {len(pairs)} pairs.")
    for pair in pairs:
        logging.debug(f"Pair: {pair}")
    return pairs


def debug_info(galaxies: set[Galaxy] = None):
    logging.debug(f"DATA size: {len(DATA)} x {len(DATA[0])}")
    logging.debug(f"Lowest x: {min(galaxies, key=lambda g: g.x)}")
    logging.debug(f"Highest x: {max(galaxies, key=lambda g: g.x)}")
    logging.debug(f"Lowest y: {min(galaxies, key=lambda g: g.y)}")
    logging.debug(f"Highest y: {max(galaxies, key=lambda g: g.y)}")



def part_one(expansion: int = 1):
    galaxies = parse_galaxies(expansion=expansion)
    pairs = make_pairs(galaxies)
    return reduce(
        operator.add,
        map(
            lambda p: abs(p[0].x - p[1].x) + abs(p[0].y - p[1].y),
            pairs
        )
    )


def part_two():
    return part_one(expansion=999999)