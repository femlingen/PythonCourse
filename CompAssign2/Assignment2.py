from enum import Enum
from random import shuffle


# TODO: ask Thomas about get_value  must be overloaded
# TODO: create from your written docstrings
# TODO: write tests
# TODO: Optional step: Create a class to represent a Player for a Texas Hold’em poker game
#

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
    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        if self.value < other:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.value == other:
            return True
        else:
            return False


class Suit(Enum):
    clubs = 0
    spades = 1
    diamonds = 2
    hearts = 3

    def __str__(self):
        return ['Clubs', 'Spades', 'Diamonds', 'Hearts'][self.value]

    def __repr__(self):
        return ['Clubs', 'Spades', 'Diamonds', 'Hearts'][self.value]


class NumberedCard(PlayingCard):
    def __init__(self, value, suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        return self.value

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)

    def __str__(self):
        return '{} of {}'.format(self.value, self.suit)


class AceCard(PlayingCard):
    def get_value(self):
        return 1

    def __repr__(self):
        return 'Ace of {}'.format(self.suit)

    def __str__(self):
        return 'Ace of {}'.format(self.suit)


class JackCard(PlayingCard):
    def get_value(self):
        return 11

    def __repr__(self):
        return 'Jack of {}'.format(self.suit)

    def __str__(self):
        return 'Jack of {}'.format(self.suit)


class QueenCard(PlayingCard):
    def get_value(self):
        return 12

    def __repr__(self):
        return 'Queen of {}'.format(self.suit)

    def __str__(self):
        return 'Queen of {}'.format(self.suit)


class KingCard(PlayingCard):
    def get_value(self):
        return 13

    def __repr__(self):
        return 'King of {}'.format(self.suit)

    def __str__(self):
        return 'King of {}'.format(self.suit)


class StandardDeck:

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

    def shuffle_cards(self):
        shuffle(self.deck_list)

    def reveal_cards(self):
        for cards in self.deck_list:
            print(cards)

    def remove_card(self):
        self.trash_pile = self.deck_list.pop()

    def deal_card(self):
        return self.deck_list.pop()

    def add_trash_card(self, trash_card):
        self.trash_pile.append(trash_card)

    def __len__(self):
        return len(self.deck_list)


class Hand:
    def __init__(self, name='Player_Name'):
        self.player_name = name
        self.cards = []

    def take_card(self, deck):
        self.hand.append(deck.deal_card())

    def drop_cards(self, deck, index=[0]):
        sorted(index)
        for indice in reversed(index):
            deck.add_trash_card(self.hand.pop(indice))




