from Assignment2 import AceCard, NumberedCard, Suit, JackCard, QueenCard, KingCard
from Assignment2 import StandardDeck, Hand, PokerHand

def test_jack():
    jack = JackCard(Suit.hearts)
    assert jack.get_value() == 11


def test_queen():
    queen = QueenCard(Suit.hearts)
    assert queen.get_value() == 12

def test_king():
    king = KingCard(Suit.hearts)
    assert king.get_value() == 13

def test_ace():
    ace = AceCard(Suit.hearts)
    assert ace.get_value() == 14

def test_nr():
    nr = NumberedCard(7 ,Suit.hearts)
    assert nr.get_value() == 7