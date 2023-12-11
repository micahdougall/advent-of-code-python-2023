from reader import get_string_data

from dataclasses import dataclass, field
import logging
import os


RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/two/{RUNTIME}.txt""")

symbols = set()
asterisks = set()


@dataclass(eq=True, frozen=True)
class EngineNumber:
    value: int
    start_position: tuple[int, int]
    length: int = field(compare=False)
    adjacents: set[tuple[int, int]] = field(compare=False)

    @staticmethod
    def pos_above(position: tuple[int, int]):
        return (position[0], position[1] - 1)
    
    @staticmethod
    def pos_below(position: tuple[int, int]):
        return (position[0], position[1] + 1)
    
    @staticmethod
    def pos_left(position: tuple[int, int]):
        return (position[0] - 1, position[1])
    
    @staticmethod
    def pos_right(position: tuple[int, int], steps=1):
        return (position[0] + steps, position[1])

    @staticmethod
    def get_adjacents(
        cls, 
        value: int, 
        start_position: tuple[int, int], 
        length: int
    ) -> set[tuple[int, int]]:
        adjacents = set()
        adjacents.add(cls.pos_left(start_position))
        for i in range(-1, length + 1):
            digit_pos = cls.pos_right(start_position, steps=i)
            adjacents.add(cls.pos_above(digit_pos))
            adjacents.add(cls.pos_below(digit_pos))
        adjacents.add(cls.pos_right(start_position, steps=length))
        logging.debug(
            f"Adjacents for {value} at {start_position}: {adjacents}"
        )
        return adjacents
    
    @classmethod
    def from_string(cls, string_num: str, start_position: tuple[int, int]):
        adjacents = cls.get_adjacents(
            cls, int(string_num), start_position, len(string_num)
        )
        return cls(int(string_num), start_position, len(string_num), adjacents)


def write_engine_to_csv(numbers: list(set[EngineNumber]), filename: str):
    with open(filename, "w") as f:
        for row in numbers:
            for num in row:
                f.write(str(num.value) + ',')
            f.write('\n')


def write_to_csv(numbers: list[list[int]], filename: str):
    with open(filename, "w") as f:
        for row in numbers:
            for num in row:
                f.write(num + ',')
            f.write('\n')


def parse_data() -> set[EngineNumber]:
    """Parse data into Number objects."""
    numbers = set()
    for y, line in enumerate(DATA):
        string_num = ""
        for x, number in enumerate(line):
            if number.isdigit():
                string_num += number   
            if not number.isdigit() or x == len(line) - 1:
                if string_num:
                    logging.debug(f"Found number: {string_num}")
                    logging.debug(f"Position: {x - len(string_num), y}")
                    num = EngineNumber.from_string(
                        string_num, 
                        (x - len(string_num), y)
                    )
                    numbers.add(num)
                    string_num = ""
                if not number.isdigit() and number != ".":
                    logging.debug(f"Found symbol: {number} at {x, y}")
                    symbols.add((x, y))
                    if number == "*":
                        logging.debug(f"Found asterisk: {number} at {x, y}")
                        asterisks.add((x, y))
    logging.debug(f"Found {len(numbers)} unique numbers.")
    logging.debug(f"Found {len(symbols)} symbols.")
    logging.debug(f"Found {len(asterisks)} asterisks.")
    return numbers


def part_one() -> list[EngineNumber]:
    """Return list of numbers that are part of the engine."""
    numbers = parse_data()
    engine_numbers = []
    for number in numbers:
        if number.adjacents.intersection(symbols):
            logging.debug(f"{number.value} has intersection: {number.adjacents.intersection(symbols)}")
            engine_numbers.append(number)
    return sum([n.value for n in engine_numbers])


def get_gears(
    connector: tuple[int, int], numbers: set[EngineNumber]
) -> EngineNumber:
    """Return partner gears if there are two adjacent numbers, else None."""
    gears = list(filter(
        lambda x: connector in x.adjacents,
        numbers
    ))
    logging.debug(f"Found {len(gears)} gears.")
    if len(gears) == 2:
        return gears[0].value * gears[1].value
    return 0


def part_two() -> list[EngineNumber]:
    """Return list of numbers that are part of the engine."""
    numbers = parse_data()
    return sum(
        [get_gears(connector, numbers) for connector in asterisks]
    )
