

import logging



def get_step_list(sequence: list[int]) -> list[int]:
    """Return list of steps from sequence."""
    return [
        sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)
    ]

def is_flat_sequence(sequence: list[int]) -> bool:
    """Return True if sequence is flat."""
    digit = sequence[0]
    for i in sequence:
        if i != digit:
            return False
    return True

def get_next_digit(sequence: list[int]) -> int:
    """Return next digit."""
    steps = [sequence]
    while not is_flat_sequence(sequence):
        sequence = get_step_list(sequence)
        steps.append(sequence)

    next_digit = 0
    while len(steps):
        sequence = steps.pop()
        sequence.append(sequence[-1] + next_digit)
        next_digit = sequence[-1]
        logging.debug(f"sequence: {sequence}")

    return sequence[-1]

def get_prev_digit(sequence: list[int]) -> int:
    """Return previous digit."""
    steps = [sequence]
    while not is_flat_sequence(sequence):
        sequence = get_step_list(sequence)
        steps.append(sequence)

    prev_digit = 0
    while len(steps):
        sequence = steps.pop()
        sequence.insert(0, sequence[0] - prev_digit)
        prev_digit = sequence[0]
        logging.debug(f"sequence: {sequence}")

    return sequence[0]


