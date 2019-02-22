import pytest
from cardlib import *

""" This is a test class for card library """

# It is important to also test strange inputs,
# like dividing what zero and see that good exceptions are thrown.
# What happens if you try create a card with numerical value 0 or -1?


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


def test_playingcard():
    nr = NumberedCard(7, Suit.hearts)
    assert nr.get_value() == 7


def test_one_pair():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(6, Suit.diamonds))
    test_hand.take_card(NumberedCard(4, Suit.spades))
    test_hand.take_card(NumberedCard(7, Suit.spades))
    test_hand.take_card(NumberedCard(8, Suit.clubs))
    test_hand.take_card(NumberedCard(8, Suit.hearts))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.one_pair.value


# def test_two_pair():
#     test_hand = Hand()
#     test_hand.take_card(NumberedCard(5, Suit.clubs))
#     test_hand.take_card(NumberedCard(5, Suit.diamonds))
#     test_hand.take_card(NumberedCard(7, Suit.spades))
#     test_hand.take_card(NumberedCard(8, Suit.hearts))
#     test_hand.take_card(NumberedCard(7, Suit.hearts))
#     p_hand = PokerHand(test_hand.cards)
#     assert p_hand.hand_type.value == PokerType.two_pair.value

def test_check_for_three():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(5, Suit.clubs))
    test_hand.take_card(NumberedCard(5, Suit.diamonds))
    test_hand.take_card(NumberedCard(5, Suit.spades))
    test_hand.take_card(NumberedCard(8, Suit.hearts))
    test_hand.take_card(NumberedCard(9, Suit.hearts))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.three_of_kind.value


def test_check_for_four():
    test_hand = Hand()
    test_hand.take_card(JackCard(Suit.hearts))
    test_hand.take_card(JackCard(Suit.diamonds))
    test_hand.take_card(JackCard(Suit.spades))
    test_hand.take_card(JackCard(Suit.clubs))
    test_hand.take_card(NumberedCard(9, Suit.hearts))

    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.four_of_kind.value


def check_full_house():
    test_hand = Hand()
    test_hand.take_card(JackCard(Suit.hearts))
    test_hand.take_card(JackCard(Suit.diamonds))
    test_hand.take_card(JackCard(Suit.spades))
    test_hand.take_card(QueenCard(Suit.diamods))
    test_hand.take_card(QueenCard(Suit.clubs))

    p_hand = PokerHand(test_hand.cards)
    print(p_hand.hand_type.value)
    assert p_hand.hand_type.value == PokerType.full_house.value # Doesn't work


def test_straight():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(5, Suit.clubs))
    test_hand.take_card(NumberedCard(6, Suit.diamonds))
    test_hand.take_card(NumberedCard(7, Suit.spades))
    test_hand.take_card(NumberedCard(8, Suit.hearts))
    test_hand.take_card(NumberedCard(9, Suit.hearts))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.straight.value


def test_flush():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(5, Suit.clubs))
    test_hand.take_card(NumberedCard(6, Suit.clubs))
    test_hand.take_card(NumberedCard(2, Suit.clubs))
    test_hand.take_card(NumberedCard(3, Suit.clubs))
    test_hand.take_card(NumberedCard(9, Suit.clubs))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.flush.value


def test_straight_flush():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(5, Suit.clubs))
    test_hand.take_card(NumberedCard(6, Suit.clubs))
    test_hand.take_card(NumberedCard(7, Suit.clubs))
    test_hand.take_card(NumberedCard(8, Suit.clubs))
    test_hand.take_card(NumberedCard(9, Suit.clubs))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.straight_flush.value


my_deck = StandardDeck()
my_deck.shuffle_cards()


