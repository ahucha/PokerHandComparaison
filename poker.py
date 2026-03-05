from collections import Counter
from itertools import combinations

class Card:
    VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, 
              "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    INV_VALUES = {v: k for k, v in VALUES.items()}
    
    def __init__(self, card_str):
        v_str = card_str[:-1]
        self.suit = card_str[-1].lower()
        self.value = self.VALUES[v_str]

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return f"{self.INV_VALUES[self.value]}{self.suit}"

class Hand:
    NAMES = {
        8: "Straight Flush", 7: "Four of a Kind", 6: "Full House", 
        5: "Flush", 4: "Straight", 3: "Three of a Kind", 
        2: "Two Pair", 1: "One Pair", 0: "High Card"
    }

    def __init__(self, cards):
        self.original_cards = cards
        self.cards = sorted(cards, key=lambda c: c.value, reverse=True)
        counts = Counter(c.value for c in self.cards)
        self.sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        
        self.category_rank = 0
        self.tie_breakers = []
        self._evaluate()
        self.chosen5 = self._get_ordered_cards()

    @classmethod
    def from_string(cls, s):
        return cls([Card(c) for c in s.split()])

    def _evaluate(self):
        values = sorted(list(set(c.value for c in self.cards)), reverse=True)
        freqs = [item[1] for item in self.sorted_counts]
        
        is_straight = False
        straight_high_card = 0

        if len(values) >= 5:
            if values[0] - values[4] == 4:
                is_straight = True
                straight_high_card = values[0]
            elif set([14, 5, 4, 3, 2]).issubset(set(values)):
                is_straight = True
                straight_high_card = 5

        is_flush = len(set(c.suit for c in self.cards)) == 1

        if is_straight and is_flush: self.category_rank = 8
        elif freqs == [4, 1]:        self.category_rank = 7
        elif freqs == [3, 2]:        self.category_rank = 6
        elif is_flush:               self.category_rank = 5
        elif is_straight:            self.category_rank = 4
        elif freqs == [3, 1, 1]:     self.category_rank = 3
        elif freqs == [2, 2, 1]:     self.category_rank = 2
        elif freqs == [2, 1, 1, 1]:  self.category_rank = 1
        else:                        self.category_rank = 0

        if is_straight:
            if straight_high_card == 5: self.tie_breakers = [5, 4, 3, 2, 1]
            else: self.tie_breakers = list(range(straight_high_card, straight_high_card - 5, -1))
        elif is_flush:
            self.tie_breakers = [c.value for c in self.cards]
        else:
            self.tie_breakers = [item[0] for item in self.sorted_counts]

    def _comparison_tuple(self):
        return (self.category_rank, *self.tie_breakers)

    def __gt__(self, other):
        return self._comparison_tuple() > other._comparison_tuple()

    def __eq__(self, other):
        if not isinstance(other, Hand): 
            return False
        return self._comparison_tuple() == other._comparison_tuple()

    def _get_ordered_cards(self):
        if self.category_rank in [8, 5, 4, 0]:
            if self.category_rank in [8, 4] and self.tie_breakers[0] == 5:
                return sorted(self.cards, key=lambda c: c.value if c.value != 14 else 1, reverse=True)
            return sorted(self.cards, key=lambda c: c.value, reverse=True)
        else:
            ordered = []
            for val, _ in self.sorted_counts:
                ordered.extend([c for c in self.cards if c.value == val])
            return ordered

    @property
    def category_name(self):
        return self.NAMES[self.category_rank]

    def __repr__(self):
        return f"{self.category_name}: {' '.join(str(c) for c in self.chosen5)}"

def resolve_game(board_str, players):
    results = []
    for name, hole in players.items():
        best = Evaluator.get_best_hand(hole, board_str)
        results.append({"name": name, "hand": best})
    results.sort(key=lambda x: x["hand"]._comparison_tuple(), reverse=True)
    best_score = results[0]["hand"]._comparison_tuple()
    return [r for r in results if r["hand"]._comparison_tuple() == best_score]

class Evaluator:
    @staticmethod
    def get_best_hand(hole_str, board_str):
        all_cards = [Card(c) for c in (hole_str + " " + board_str).split()]
        possible_5_card_hands = [Hand(list(combo)) for combo in combinations(all_cards, 5)]
        return max(possible_5_card_hands)