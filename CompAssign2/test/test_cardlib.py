from cardlib import AceCard, NumberedCard, Suit, JackCard, QueenCard, KingCard
from cardlib import StandardDeck, Hand, PokerHand


def test_suit_class():
    assert Suit.clubs != Suit.diamonds and Suit.hearts != Suit.diamonds
    assert Suit.spades != Suit.hearts and Suit.spades != Suit.diamonds

# två händer med två specifika fall samt lägga upp några kort på bordet och veta vad som ska
# returneras. Testa fallen och se så att vi vet att vi får rätt


def test_playingcard():
    # do some shit
    assert 1 == 1


def test_jack():
    jack = JackCard(Suit.hearts)
    assert jack.get_value() == 11


def test_queen():
    queen = QueenCard(Suit.hearts)
    assert queen.get_value() == 12


def test_king():
    king = KingCard(Suit.hearts)
    assert king.get_value() == 13


def test_ace_card():
    ace = AceCard(Suit.hearts)
    assert ace.get_value() == 14


def test_playingcard():
    nr = NumberedCard(7 ,Suit.hearts)
    assert nr.get_value() == 7
