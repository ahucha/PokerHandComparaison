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