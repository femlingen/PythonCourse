from enum import Enum
from random import shuffle
from collections import Counter  # Counter is convenient for counting objects (a specialized dictionary)
import copy


# TODO: ask Thomas about get_value must be overloaded
# TODO ask about the comparison operators
# TODO: create from your written docstrings
# TODO: write tests
# TODO: Optional step: Create a class to represent a Player for a Texas Hold’em poker game


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

    def take_card(self, card):
        self.cards.append(card)

    def drop_cards(self, index=None):
        if index is None:
            return False
        sorted(index)
        for i1 in reversed(index):
            self.cards.pop(i1)

    def reveal_cards(self):
        msg = 'The hand includes: ' + str(self.cards)
        print(msg)

    def sort_hand(self):
        self.cards.sort()

    """ There must also be a method  best_poker_hand( self , cards=[])  which computes the best 
    hand out of the cards in the hand and cards in the input argument. The  best_poker_hand  method returns 
    a  PokerHand . It should be able to handle a total of more than 5 cards (as is the case in Texas Hold ’em). """

    def best_poker_hand(self, cards=[]):
        # should return a pokerhand
        pass


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


class PokerType(Enum):

    straight_flush = 8
    four_of_kind = 7
    full_house = 6
    flush = 5
    straight = 4
    three_of_kind = 3
    two_pair = 2
    one_pair = 1
    high_card = 0

    def __lt__(self, other):
        pass #TODO

    def __eq__(self, other):
        pass #TODO


class PokerHand:

    def __init__(self, poker_hand):
        cards = poker_hand
        cards.sort()

        checks = [PokerHand.check_straight_flush, PokerHand.check_foak, PokerHand.check_full_house,
                  PokerHand.check_flush, PokerHand.check_straight, PokerHand.check_for_three,
                  PokerHand.check_two_pair, PokerHand.check_pair, PokerHand.check_high_card]

        for check, htype in zip(checks, PokerType): # looping over functions since they could be see as objects.
            # Uses zip to compare two lists values
            tmp = check(cards)
            if tmp is not None:
                self.high_card = tmp
                self.hand_type = htype
                break

    @staticmethod
    def check_high_card(cards):
        card = cards[-1]
        return card.get_value()

    @staticmethod
    def check_pair(cards):
        for i in range(len(cards)-1):
            if cards[i].get_value() == cards[i+1].get_value():
                return cards[i].get_value()

    @staticmethod
    def check_two_pair(cards):
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        two_pair = [v[0] for v in value_count.items() if v[1] >= 2]
        two_pair.sort(reverse=True)
        if len(two_pair) > 1:
            return two_pair[0], two_pair[1]

    @staticmethod
    def check_for_three(cards):
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()

        if len(threes) > 0:
            return threes[0] # maybe not the right way of returning the value

    @staticmethod
    def check_straight(cards):
        vals = [c.get_value() for c in cards]
        for c in reversed(cards):  # Starting point (high card)
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    break

            if found_straight:
                high_card = cards[0]
                return high_card.get_value()

    @staticmethod
    def check_flush(cards):
        temp_list = []
        cnt = Counter()
        for card in cards:
            cnt[card.suit] += 1
        if cnt.most_common(1)[0][1] > 4:
            for card1 in reversed(cards):
                if card1.suit == cnt.most_common(1)[0][0]:
                    temp_list.append(card1)
                    if len(temp_list) == 5:
                        break
            return card1.get_value()

    @staticmethod
    def check_foak(cards):
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        fours = [v[0] for v in value_count.items() if v[1] >= 4]
        if len(fours) > 0:  # double checking it
            return fours[0]

    @staticmethod
    def check_straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)

        :param cards: A list of playing cards.
        :return: None if no straight flush is found, else the value of the top card.
        """
        vals = [(c.get_value(), c.suit) for c in cards] \
            + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value()

    @staticmethod
    def check_full_house(cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)

        :param cards: A list of playing cards
        :return: None if no full house is found, else a tuple of the values of the triple and pair.
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
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


my_deck = StandardDeck()
my_deck.shuffle_cards()
my_hand = Hand()
my_hand.take_card(NumberedCard(8, Suit.hearts))
my_hand.take_card(NumberedCard(2, Suit.diamonds))
my_hand.take_card(NumberedCard(2, Suit.clubs))
my_hand.take_card(JackCard(Suit.hearts))
my_hand.take_card(JackCard(Suit.diamonds))
my_hand.take_card(KingCard(Suit.hearts))
my_hand.sort_hand()
my_hand.reveal_cards()

# TODO: Vi tog bort att take card tog en deck som argument för att i nästa uppgift skall det bli mycket
# enklare såhär får att dealern skall kunna ge kort till "händer" så istället bör det kallas på att vår deck
# skall deala ett kort till handen

ph = PokerHand(my_hand.cards)
print(ph.hand_type.value)
print(PokerType.full_house.value)



