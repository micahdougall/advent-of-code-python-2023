from reader import get_string_data

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key, reduce
import logging
import math
import operator
import os

file = __file__.split("/")[-1].split(".")[0]
RUNTIME = os.environ.get("RUNTIME")
DATA = get_string_data(f"""res/{file}/{RUNTIME}.txt""")


class Type(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


CARDS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

@dataclass
class Hand:
    cards: str
    bid: int
    wild: bool = False
    type: Type = None

    def __post_init__(self):
        self.type = (
            self.get_type() 
            if not self.wild or "J" not in self.cards 
            else self.get_wild_type()
        )
        logging.info(f"Hand type: {self.type} for {self.cards}")

    def get_type(self):
        counter = Counter(self.cards)
        # logging.debug(f"Counter: {counter}")
        # logging.debug(f"Length of counter: {len(counter)}")
        if len(counter) == 5:
            return Type.HIGH_CARD
        if len(counter) == 1:
            return Type.FIVE_OF_A_KIND
        if len(counter) == 2:
            if 3 in counter.values():
                return Type.FULL_HOUSE
            else:
                return Type.FOUR_OF_A_KIND
        if len(counter) == 3:
            if 3 in counter.values():
                return Type.THREE_OF_A_KIND
            else:
                return Type.TWO_PAIR
        return Type.PAIR

    def get_wild_type(self):
        counter = Counter(self.cards)
        # logging.debug(f"Counter: {counter}")
        # logging.debug(f"Length of counter: {len(counter)}")
        if len(counter) == 2:
            return Type.FIVE_OF_A_KIND
        if len(counter) == 3:
            if 3 in counter.values() or counter["J"] == 2:
                return Type.FOUR_OF_A_KIND
            else:
                return Type.FULL_HOUSE
        if len(counter) == 4:
            return Type.THREE_OF_A_KIND
        return Type.PAIR
    

def compare_cards(card_one: str, card_two: str):
    # logging.debug(f"Comparing cards: {card_one} and {card_two}")
    for i in range(len(card_one)):
        if CARDS.get(card_one[i]) > CARDS.get(card_two[i]):
            logging.debug(f"Card one is better: {card_one[i]} > {card_two[i]}")
            return -1
        elif CARDS.get(card_one[i]) < CARDS.get(card_two[i]):
            logging.debug(f"Card two is better: {card_one[i]} < {card_two[i]}")
            return 1


def compare_hands(hand_one: Hand, hand_two: Hand):
    # logging.debug(f"Comparing hands: {hand_one.cards} and {hand_two.cards}")
    if hand_one.type.value > hand_two.type.value:
        logging.debug(f"Hand one is better: {hand_one.type} > {hand_two.type}")
        return -1
    elif hand_one.type.value < hand_two.type.value:
        logging.debug(f"Hand two is better: {hand_one.type} < {hand_two.type}")
        return 1
    else:
        return compare_cards(hand_one.cards, hand_two.cards)


def parse_data(wild: bool = False):
    hands = []
    for line in DATA:
        cards, bid = line.split(" ")
        hands.append(Hand(cards=cards, bid=int(bid), wild=wild))
    return hands


def get_winnings(hands: list):
    for hand in hands:
        logging.debug(f"Hand: {hand}")
    hands_sorted = sorted(hands, key=cmp_to_key(compare_hands))
    # logging.debug(f"Hands sorted: {[card.cards for card in hands_sorted]}")

    ranks = range(len(hands_sorted), 0, -1)
    winnings = 0
    for i, hand in enumerate(hands_sorted):
        winnings += hand.bid * ranks[i]
    return winnings


def part_one():
    hands = parse_data()
    return get_winnings(hands)


def part_two():
    CARDS["J"] = 1
    hands = parse_data(wild=True)
    return get_winnings(hands)