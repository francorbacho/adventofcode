#!/usr/bin/env python
#
# 251536706 is too high

import collections
import fileinput

CARDS_WITHOUT_J = "23456789TQKA"
CARDS = "J23456789TQKA"
BASE = 1000

def calculate_power(card: str, real_card: str | None = None) -> int:
    if real_card is None:
        real_card = card

    assert 'J' not in card
    howmanyofeach = {c: card.count(c) for c in set(card)}
    singles_pairs_etc = sorted(list(howmanyofeach.values()), reverse=True)
    singles_pairs_etc = {c: singles_pairs_etc.count(c) for c in set(singles_pairs_etc)}
    power = 0
    for i in range(5, 0, -1):
        power *= BASE
        power += singles_pairs_etc[i] if i in singles_pairs_etc else 0

    card_ = real_card
    for c in real_card:
        power *= BASE
        power += (CARDS.find(c) + 1)
        card_ = card_[1:]

    return power

def maximize_card_power(hand: str, real_hand: str | None = None) -> int:
    if real_hand is None:
        real_hand = hand
    if 'J' not in hand:
        return calculate_power(hand, real_hand)
    max_power = 0
    for card in CARDS_WITHOUT_J:
        new_hand = hand.replace('J', card, 1)
        max_power = max(max_power, maximize_card_power(new_hand, real_hand))
    return max_power

class CardBidPair:
    def __init__(self, card: str, bid: int) -> None:
        self.card = card
        self.bid = bid
        if 'J' in card:
            self.power = maximize_card_power(card, card)
        else:
            self.power = calculate_power(card, card)

    def __repr__(self) -> str:
        return f"{self.card}/{self.power}"

lines = [line.split(' ') for line in fileinput.input()]
pairs = [CardBidPair(line[0], int(line[1])) for line in lines]
pairs.sort(key=lambda v: v.power)
print("\n".join(f"{pair.card} — {pair.power}" for pair in pairs))

res = 0
for i, cardbid in enumerate(pairs):
    res += (i + 1) * cardbid.bid

print(f"res :: {res}")
