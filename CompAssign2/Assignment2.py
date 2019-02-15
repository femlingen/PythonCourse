from enum import Enum
from random import shuffle
from collections import Counter  # Counter is convenient for counting objects (a specialized dictionary)
import copy


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
    """
    A general class for all cards made
    """
    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __eq__(self, other):
        return self.get_value() == other.get_value()

    def __gt__(self, other):
        return self.get_value() > other.get_value()


class Suit(Enum):
    """
    A class for avoiding mistakes while using suits
    """
    clubs = 0
    spades = 1
    diamonds = 2
    hearts = 3

    def __repr__(self):
        return self.name.capitalize()

    def __str__(self):
        return self.name.capitalize()



class NumberedCard(PlayingCard):
    """
    A class for making card objects between and including value 2 and 10
    """
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
    """
    A class for making Ace cards
    """

    @staticmethod
    def get_value():
        return 14

    def __str__(self):
        return 'Ace of {}'.format(self.suit)

    def __repr__(self):
        return 'Ace of {}'.format(self.suit)


class JackCard(PlayingCard):
    """
    A class for making Jack cards
    """

    @staticmethod
    def get_value():
        return 11

    def __str__(self):
        return 'Jack of {}'.format(self.suit)

    def __repr__(self):
        return 'Jack of {}'.format(self.suit)


class QueenCard(PlayingCard):
    """
    A class for making Queen cards
    """
    @staticmethod
    def get_value():
        return 12

    def __str__(self):
        return 'Queen of {}'.format(self.suit)

    def __repr__(self):
        return 'Queen of {}'.format(self.suit)


class KingCard(PlayingCard):
    """
    A class for making King cards
    """
    @staticmethod
    def get_value():
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
    """
    A class for creating a hand (player) object that can draw cards from a deck to it
    :return: Returns a list of standard deck of cards
    """

    def __init__(self, name='Player_Name'):
        self.player_name = name
        self.cards = []

    def take_card(self, deck):
        self.cards.append(deck.deal_card())

    def drop_cards(self, deck, index=None):
        if index is None:
            index = [0]
        sorted(index)
        for i1 in reversed(index):
            deck.add_trash_card(self.cards.pop(i1))

    def reveal_cards(self):
        msg = 'The hand includes: ' + ''.join(str(self.cards))
        print(msg)

    def sort_hand(self):
        self.cards.sort()


""" Task 3 - The deck:  A  StandardDeck ()  must create a full deck of (52) cards. 
There should be functions for shuffling and taking the top card (which removes the card from the deck). """


class StandardDeck:
    """
    A class for creating and altering decks
    :return: Returns a list of standard deck of cards
    """

    def __init__(self):
        self.trash_pile = []
        self.deck_list = []
        suit_list = [Suit.spades, Suit.diamonds, Suit.clubs, Suit.hearts]

        for suit in Suit:
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


class PokerHand:
    def __init__(self, poker_hand):
        self.cards = poker_hand
        self.cards.sort()
        self.best_hand = None
        self.high_card = None
        self.hand_type = None
        self.check_hand()

    def check_hand(self):
        # Go through all functions and calculate values
        self.check_high_card()
        self.check_pair()
        self.check_toak()
        self.check_foak()
        self.check_straight()
        #  check_high_card(cards)

    def check_high_card(self):
        max_card = self.cards[0]
        for card in self.cards:
            if max_card < card:
                max_card = card
        self.best_hand = max_card
        self.high_card = max_card
        self.hand_type = 'High Card'

    def check_pair(self):
        for card1 in self.cards:
            for card2 in self.cards:
                if card1.get_value == card2.get_value and card1.suit != card2.suit:
                    self.best_hand = [card1, card2]
                    self.hand_type = 'Pair'

    def check_two_pair(self):
        pass

    def check_toak(self): #three of a kind
        for i1, card in enumerate(self.cards[0:-3]):
            if card.get_value == self.cards[i1+2].get_value():
                self.best_hand = self.cards[i1:i1+3]
                self.hand_type = 'Three of a kind'

    def check_straight(self):
        for i1, card in enumerate(self.cards[0:-4]):
            card_value = card.value
            for i2 in range(1, 5):
                if self.cards[i1+i2] == 1:
                    pass
                # TODO: Fix method

    def check_flush(self):
        pass

    def check_foak(self):  # four of a kind
        for i1, card in enumerate(self.cards[0:-4]):
            if card.get_value == self.cards[i1+3].get_value:
                self.best_hand = self.cards[i1:i1+4]
                self.hand_type = 'Four of a kind'


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

    def __repr__(self):
        return '{}'.format(self.best_hand)


my_deck = StandardDeck()
my_deck.shuffle_cards()
my_hand = Hand()
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)
my_hand.take_card(my_deck)

my_hand.sort_hand()
my_hand.reveal_cards()

ph = PokerHand(my_hand.cards)
print(ph.best_hand)
print(ph.hand_type)