from collections import Counter
from itertools import combinations

class Card:
    VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, 
              "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    
    def __init__(self, card_str):
        v_str = card_str[:-1]
        self.suit = card_str[-1].lower()
        self.value = self.VALUES[v_str]

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return f"{self.value}{self.suit}"

class Hand:
    def __init__(self, cards):
        self.cards = sorted(cards, key=lambda c: c.value, reverse=True)
        counts = Counter(c.value for c in self.cards)
        self.sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        
        self.category_rank = 0
        self.tie_breakers = []
        self._evaluate()

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

        if is_straight:
            self.category_rank = 4
            if straight_high_card == 5:
                self.tie_breakers = [5, 4, 3, 2, 1]
            else:
                self.tie_breakers = list(range(straight_high_card, straight_high_card - 5, -1))
        
        elif freqs == [4, 1]: self.category_rank = 7
        elif freqs == [3, 2]: self.category_rank = 6
        elif freqs == [3, 1, 1]: self.category_rank = 3
        elif freqs == [2, 2, 1]: self.category_rank = 2
        elif freqs == [2, 1, 1, 1]: self.category_rank = 1
        else: self.category_rank = 0 

        if not self.tie_breakers:
            self.tie_breakers = [item[0] for item in self.sorted_counts]

    def _comparison_tuple(self):
        return (self.category_rank, *self.tie_breakers)

    def __gt__(self, other):
        return self._comparison_tuple() > other._comparison_tuple()

    def __eq__(self, other):
        if not isinstance(other, Hand):
            return False
        return self._comparison_tuple() == other._comparison_tuple()


class Evaluator:
    @staticmethod
    def get_best_hand(hole_str, board_str):
        all_cards = [Card(c) for c in (hole_str + " " + board_str).split()]
        
        possible_5_card_hands = []
        for combo in combinations(all_cards, 5):
            possible_5_card_hands.append(Hand(list(combo)))
        
        return max(possible_5_card_hands)