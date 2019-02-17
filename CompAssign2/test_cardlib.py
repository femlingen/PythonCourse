import pytest
from Assignment2 import *


def test_math():
    assert 1 + 1 == 2
    assert 2 * 2 + 3 == 7
    # It is important to also test strange inputs,
    # like dividing what zero and see that good exceptions are thrown.
    # What happens if you try create a card with numerical value 0 or -1?

# no idea what I am testing. Testing the tests. Hehe
def test_suit_class():
    assert Suit.clubs != Suit.diamonds and Suit.hearts != Suit.diamonds
    assert Suit.spades != Suit.hearts and Suit.spades != Suit.diamonds

def test_playingcard():
    # do some shit
    assert 1 == 1


def test_ace_card():
    assert AceCard.get_value() == 14


def test_king_card():
    assert KingCard.get_value() == 13


def test_queen_card():
    assert QueenCard.get_value() == 12


def test_jack_card():
    assert JackCard.get_value() == 11


def test_numbered_card():
    assert 1 == 1
    # do some shit


def test_hand():
    """
    Creating an empty hand and tries to drop cards from it
    """
    test_hand = Hand()
    test_deck = StandardDeck()
    assert test_hand.drop_cards(test_deck) == False



    # TODO: test if the card we picked was removed from the deck


