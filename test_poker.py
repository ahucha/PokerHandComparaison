from poker import Card
from poker import Hand

def test_card_creation():
    c = Card("As")
    assert c.value == 14
    assert c.suit == "s"

def test_card_comparison():
    c1 = Card("Kh") 
    c2 = Card("2d")
    assert c1 > c2

def test_straight_normal():

    h_straight = Hand.from_string("9s 8h 7d 6c 5s")
    assert h_straight.category_rank == 4
    assert h_straight._comparison_tuple() == (4, 9, 8, 7, 6, 5)

def test_straight_ace_low_wheel():
    h_wheel = Hand.from_string("As 2h 3d 4c 5s")
    assert h_wheel.category_rank == 4
    assert h_wheel._comparison_tuple() == (4, 5, 4, 3, 2, 1)