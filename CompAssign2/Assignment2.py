
""" This is an assignment in course Object Oriented Programming in Python - DAT171 """
__author__ = "Lucas Jutvik & Frida Femling"


"""" 
The task is set up as a top-down design, where the top level functions are written before 
the core functionality is implemented. Insert placeholders as you go along!
You are not required to follow the provided task order. On the next page are a 
specifications of what is required of your library.
"""


# --- Variable declaration ---


class Card(object):

    suit_names = ["Clubs", "Hearts", "Diamond","Spades" ]
    card_number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]


    def __init__(self, suit_name, card_number):
        self.self = self
        self.suit_names = suit_name
        self.card_number = card_number

    def print_card_number(self):
        return(self.card_number)

#testing
my_card = Card("Clubs", "Jack")
print(my_card.print_card_number())
