from reader import get_string_data

from dataclasses import dataclass
import logging
import math
import os

RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/four/{RUNTIME}.txt""")


@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    guessed_numbers: list[int]
    count: int = 1

    def matched_cards(self) -> int:
        return len(set(self.winning_numbers) & set(self.guessed_numbers))

    def score(self) -> int:
        matched = self.matched_cards()
        logging.debug(f"Matched cards for card {self.id}: {matched}")
        score = int(0 if not matched else 1 * math.pow(2, matched - 1))
        logging.debug(f"Score: {score}")
        return score


def parse_cards() -> list[Card]:
    cards = []
    for card in DATA:
        card_id, numbers = card.split(": ")
        winning, guessed = numbers.split(" | ")
        winning_numbers = [int(n) for n in winning.split()]
        logging.debug(f"Winning numbers: {winning_numbers}")
        guessed_numbers = [int(n) for n in guessed.split()]
        logging.debug(f"Guessed numbers: {guessed_numbers}")
        cards.append(
            Card(int(card_id[5:]), winning_numbers, guessed_numbers)
        )
    logging.debug(f"Cards: {cards}")
    return cards


def part_one():
    cards = parse_cards()
    return sum([card.score() for card in cards])


def part_two():
    cards = {card.id: card for card in parse_cards()}
    for id, card in cards.items():
        logging.debug(f"Card {id} has {card.matched_cards()} matches.")
        logging.debug(f"Card {id} has {card.count} copies.")
        for i in range(1, card.matched_cards() + 1):
            logging.debug(f"Copying card {cards[id + i].id}")
            cards[card.id + i].count += card.count
    for card in cards.values():
        logging.debug(f"Card {card.id} has a count of {card.count}")
    return sum([card.count for card in cards.values()])