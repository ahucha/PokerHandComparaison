from poker import Card

def test_card_creation():
    c = Card("As")
    assert c.value == 14
    assert c.suit == "s"

def test_card_comparison():
    c1 = Card("Kh") 
    c2 = Card("2d")
    assert c1 > c2