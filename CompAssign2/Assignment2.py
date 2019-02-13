from enum import Enum
from random import shuffle
from collections import Counter  # Counter is convenient for counting objects (a specialized dictionary)


# TODO: ask Thomas about get_value must be overloaded
# TODO: create from your written docstrings
# TODO: write tests
# TODO: Optional step: Create a class to represent a Player for a Texas Hold’em poker game
# TODO: Ask about get_value static, do they have to be methods?

""" This is an assignment in course Object Oriented Programming in Python - DAT171 """
__author__ = "Lucas Jutvik & Frida Femling"


"""" 
The task is set up as a top-down design, where the top level functions are written before 
the core functionality is implemented. Insert placeholders as you go along!
You are not required to follow the provided task order. On the next page are a 
specifications of what is required of your library.
"""


# --- Variable declaration ---


class PlayingCard:
    """A general class for all cards made"""
    def __init__(self, suit):
        self.suit = suit


class Suit(Enum):
    """A class for avoiding mistakes while using suits"""
    clubs = 0
    spades = 1
    diamonds = 2
    hearts = 3

    def __str__(self):
        return ['Clubs', 'Spades', 'Diamonds', 'Hearts'][self.value]

    def __repr__(self):
        return ['Clubs', 'Spades', 'Diamonds', 'Hearts'][self.value]


class NumberedCard(PlayingCard):
    """A class for making card objects between and including value 2 and 10"""
    def __init__(self, value, suit):
        super().__init__(suit)  # goes down to PlayingCard-class to fetch PlayingCard
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return '{} of {}'.format(self.value, self.suit)

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)


class AceCard(PlayingCard):
    """A class for makin Ace cards"""
    def get_value(self):
        return 1

    def __str__(self):
        return 'Ace of {}'.format(self.suit)

    def __repr__(self):
        return 'Ace of {}'.format(self.suit)


class JackCard(PlayingCard):
    """A class for making Jack cards"""
    def get_value(self):
        return 11

    def __str__(self):
        return 'Jack of {}'.format(self.suit)

    def __repr__(self):
        return 'Jack of {}'.format(self.suit)


class QueenCard(PlayingCard):
    """A class for making Queen cards"""
    def get_value(self):
        return 12

    def __str__(self):
        return 'Queen of {}'.format(self.suit)

    def __repr__(self):
        return 'Queen of {}'.format(self.suit)


class KingCard(PlayingCard):
    """A class for making King cards"""
    def get_value(self):
        return 13

    def __str__(self):
        return 'King of {}'.format(self.suit)

    def __repr__(self):
        return 'King of {}'.format(self.suit)


"""
Task 2: The  Hand  must have methods for adding a new card, dropping several cards (based on an index list), 
and sorting the cards. There must also be a method  best_poker_hand( self , cards=[])  
which computes the best hand out of the cards in the hand and cards in the input argument. 
The  best_poker_hand  method returns a  PokerHand . """


class Hand:
    """A class for creating a hand (player) object that can draw cards from a deck to it"""
    def __init__(self, name='Player_Name'):
        self.player_name = name
        self.cards = []

    def take_card(self, deck):
        self.cards.append(deck.deal_card())

    def drop_cards(self, deck, index=None):
        if index == None:
            index = [0]
        sorted(index)
        for i1 in reversed(index):
            deck.add_trash_card(self.cards.pop(i1))

    def reveal_cards(self):
        for card in self.cards:
            print(card)


""" Task 3 - The deck:  A  StandardDeck ()  must create a full deck of (52) cards. 
There should be functions for shuffling and taking the top card (which removes the card from the deck). """


class StandardDeck:
    """A class for creating and altering decks"""
    def __init__(self):
        self.trash_pile = []
        self.deck_list = []
        suit_list = [Suit.spades, Suit.diamonds, Suit.clubs, Suit.hearts]

        for suit in suit_list:
            self.deck_list.append(AceCard(suit))
            for counter in range(2, 11):
                self.deck_list.append(NumberedCard(counter, suit))
            self.deck_list.append(JackCard(suit))
            self.deck_list.append(QueenCard(suit))
            self.deck_list.append(KingCard(suit))

    def shuffle_cards(self):  # shuffled from random library
        shuffle(self.deck_list)

    def reveal_cards(self):
        for cards in self.deck_list:
            print(cards)

    def remove_card(self):
        self.trash_pile.append(self.deck_list.pop())

    def deal_card(self):
        return self.deck_list.pop()

    def add_trash_card(self, trash_card):
        self.trash_pile.append(trash_card)

    def __len__(self):
        return len(self.deck_list)


""" The poker hand  (for a lack of a better name): A  PokerHand  should contain a hand object 
(high card, one pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush) 
and the highest value(s) (and perhaps suits). The  PokerHand should overload the < operator in order to compare 
which  PokerHand  is valued highest based on the type, value(s) (and possible suit)."""
# TODO: Want to add these in a separate file

# TODO: Är det meningen att vi ska inherita från Hand? Hur ser konstruktorn ut?


class PokerHand(Hand):
    def __init__(self, poker_hand):
        self.cards = poker_hand

    def check_hand(self):
        # Go through all functions and calculate values
        pass
        #  check_high_card(cards)


def check_high_card(cards):
    pass


def check_pair(cards):
    pass


def check_two_pair(cards):
    pass


def check_toak(cards): #three of a kind
    pass


def check_straight(cards):
    pass


def check_flush(cards):
    pass


def check_foak(cards):  # four of a kind
    pass


def check_straight_flush(cards):
    """
    Checks for the best straight flush in a list of cards (may be more than just 5)

    :param cards: A list of playing cards.
    :return: None if no straight flush is found, else the value of the top card.
    """
    vals = [(c.give_value(), c.suit) for c in cards] \
        + [(1, c.suit) for c in cards if c.give_value() == 14]  # Add the aces!
    for c in reversed(cards):  # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1, 5):
            if (c.give_value() - k, c.suit) not in vals:
                found_straight = False
                break
        if found_straight:
            return c.give_value()


def check_full_house(cards):
    """
    Checks for the best full house in a list of cards (may be more than just 5)

    :param cards: A list of playing cards
    :return: None if no full house is found, else a tuple of the values of the triple and pair.
    """
    value_count = Counter()
    for c in cards:
        value_count[c.give_value()] += 1
    # Find the card ranks that have at least three of a kind
    threes = [v[0] for v in value_count.items() if v[1] >= 3]
    threes.sort()
    # Find the card ranks that have at least a pair
    twos = [v[0] for v in value_count.items() if v[1] >= 2]
    twos.sort()

    # Threes are dominant in full house, lets check that value first:
    for three in reversed(threes):
        for two in reversed(twos):
            if two != three:
                return three, two
