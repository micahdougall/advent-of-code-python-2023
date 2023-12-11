import logging




def get_outer_digits(sequence: str) -> int:
    """Return list of outer digits."""
    logging.debug(f"sequence: {sequence}")

    digits = [i for i in sequence if i.isdigit()]
    logging.debug(f"digits: {digits}")
    return int(digits[0] + digits[-1])


def get_outer_str_digits(sequence: str) -> int:
    """Return list of outer digits."""
    logging.debug(f"sequence: {sequence}")

    numbers = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    while (
        sequence
        and not sequence.startswith(tuple(numbers.keys()))
        and not sequence[0].isdigit()
    ):
        sequence = sequence[1:]
        logging.debug(f"sequence: {sequence}")
    if sequence[0].isdigit():
        first_digit = sequence[0]
    else:
        str_len = 3
        str_digit = sequence[:str_len]
        while not str_digit in numbers.keys():
            str_len += 1
            str_digit = sequence[:str_len]
        first_digit = numbers.get(str_digit)
    logging.debug(f"first_digit: {first_digit}")

    while (
        sequence
        and not sequence.endswith(tuple(numbers.keys()))
        and not sequence[-1].isdigit()
    ):
        sequence = sequence[:-1]
        logging.debug(f"sequence: {sequence}")
    if sequence[-1].isdigit():
        last_digit = sequence[-1]
    else:
        str_len = 3
        str_digit = sequence[-str_len:]
        while not str_digit in numbers.keys() and str_len < len(sequence):
            str_len += 1
            str_digit = sequence[-str_len:]
        last_digit = numbers.get(str_digit)
    logging.debug(f"last_digit: {last_digit}")
    
    return int(first_digit + last_digit)
