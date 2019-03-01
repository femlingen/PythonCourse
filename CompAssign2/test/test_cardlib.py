from CompAssign3.cardlib import *

""" This is a test class for card library """

# It is important to also test strange inputs,
# like dividing what zero and see that good exceptions are thrown.
# What happens if you try create a card with numerical value 0 or -1?


def test_ace_card(): # Some base tests on the cards
    assert AceCard.get_value() == 14


def test_king_card():
    assert KingCard.get_value() == 13


def test_queen_card():
    assert QueenCard.get_value() == 12


def test_jack_card():
    assert JackCard.get_value() == 11


def test_playingcard():
    nr = NumberedCard(7, Suit.hearts)
    assert nr.get_value() == 7


def test_hand():  # some base test on the Hand() class
    test_hand = Hand()
    test_hand.take_card(my_deck.deal_card())
    assert len(test_hand.cards) != 0


def test_dropping_cards():
    test_hand = Hand()
    test_hand.take_card(my_deck.deal_card())
    test_hand.drop_cards([0])
    assert len(test_hand.cards) == 0


def test_dropping_cards_2():
    test_hand = Hand()
    assert test_hand.drop_cards([0]) == False


def test_one_pair(): # testing as we go
    test_hand = Hand()
    test_hand.take_card(NumberedCard(6, Suit.diamonds))
    test_hand.take_card(NumberedCard(4, Suit.spades))
    test_hand.take_card(NumberedCard(7, Suit.spades))
    test_hand.take_card(NumberedCard(8, Suit.clubs))
    test_hand.take_card(NumberedCard(8, Suit.hearts))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.one_pair.value


def test_two_pair():
    test_hand = Hand()
    test_hand.take_card(NumberedCard(5, Suit.clubs))
    test_hand.take_card(NumberedCard(5, Suit.diamonds))
    test_hand.take_card(NumberedCard(7, Suit.spades))
    test_hand.take_card(NumberedCard(8, Suit.hearts))
    test_hand.take_card(NumberedCard(7, Suit.hearts))
    p_hand = PokerHand(test_hand.cards)
    assert p_hand.hand_type.value == PokerType.two_pair.value


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
    assert p_hand.hand_type.value == PokerType.full_house.value


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


# should return a straight
def test_best_poker_hand():
    hand_cards = Hand()
    tb_cards = [NumberedCard(8, Suit.spades),NumberedCard(9, Suit.spades),NumberedCard(10, Suit.diamonds)]

    hand_cards.take_card(JackCard(Suit.spades))
    hand_cards.take_card(QueenCard(Suit.spades))

    p_h = hand_cards.best_poker_hand(tb_cards)

    assert p_h.hand_type.value == PokerType.straight.value


def test_same_pair():
    pair_one = Hand()
    pair_two = Hand()

    tb_cards = [JackCard(Suit.diamonds), QueenCard(Suit.diamonds), NumberedCard(6, Suit.diamonds)]

    pair_one.take_card(JackCard(Suit.spades))
    pair_one.take_card(NumberedCard(2, Suit.spades))

    pair_two.take_card(NumberedCard(2, Suit.hearts))
    pair_two.take_card(JackCard(Suit.hearts))

    p_h1 = pair_one.best_poker_hand(tb_cards)
    p_h2 = pair_two.best_poker_hand(tb_cards)

    assert p_h1.hand_type.value == p_h2.hand_type.value


def test_two_pair_against_one_pair():
    two_pair_hand = Hand()
    one_pair_hand = Hand()

    tb_cards = [JackCard(Suit.diamonds),QueenCard(Suit.diamonds),NumberedCard(2, Suit.diamonds)]

    two_pair_hand.take_card(JackCard(Suit.spades))
    two_pair_hand.take_card(NumberedCard(2, Suit.spades))

    one_pair_hand.take_card(NumberedCard(2, Suit.hearts))
    one_pair_hand.take_card(NumberedCard(10, Suit.diamonds))

    p_h1 = two_pair_hand.best_poker_hand(tb_cards)
    p_h2 = one_pair_hand.best_poker_hand(tb_cards)

    assert p_h1.hand_type.value > p_h2.hand_type.value

def test_full_house_against_straight():
    full_house_hand = Hand()
    straight_hand = Hand()

    tb_cards = [JackCard(Suit.diamonds), QueenCard(Suit.diamonds), QueenCard(Suit.hearts), NumberedCard(10,Suit.spades)]

    full_house_hand.take_card(JackCard(Suit.spades))
    full_house_hand.take_card(QueenCard(Suit.spades))

    straight_hand.take_card(NumberedCard(9, Suit.hearts))
    straight_hand.take_card(NumberedCard(8, Suit.diamonds))

    p_h1 = full_house_hand.best_poker_hand(tb_cards)
    p_h2 = straight_hand.best_poker_hand(tb_cards)

    assert p_h1.hand_type.value > p_h2.hand_type.value





