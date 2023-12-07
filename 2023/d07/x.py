#!/usr/bin/env python

import collections
import fileinput

CARDS = "23456789TJQKA"
BASE = 1000

def calculate_power(card: str) -> int:
    howmanyofeach = {c: card.count(c) for c in set(card)}
    singles_pairs_etc = sorted(list(howmanyofeach.values()), reverse=True)
    singles_pairs_etc = {c: singles_pairs_etc.count(c) for c in set(singles_pairs_etc)}
    power = 0
    for i in range(5, 0, -1):
        power *= BASE
        power += singles_pairs_etc[i] if i in singles_pairs_etc else 0

    card_ = card
    for c in card:
        power *= BASE
        power += (CARDS.find(c) + 1)
        card_ = card_[1:]

    return power

class CardBidPair:
    def __init__(self, card: str, bid: int) -> None:
        self.card = card
        self.bid = bid
        self.power = calculate_power(card)

    def __repr__(self) -> str:
        return f"{self.card}/{self.power}"

lines = [line.split(' ') for line in fileinput.input()]
pairs = [CardBidPair(line[0], int(line[1])) for line in lines]
pairs.sort(key=lambda v: v.power)

res = 0
for i, cardbid in enumerate(pairs):
    res += (i + 1) * cardbid.bid

print(f"res :: {res}")
