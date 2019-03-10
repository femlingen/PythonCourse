from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
import sys
from CompAssign3.card_view import *
from CompAssign3.Hold_Em_View import *



# The following shows hidden (excepted) error messages from pyqt5
###
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook
###

class PotModel(QObject):
    """
    The pot model handles all the logic regarding the pot and also sends signals to the view to change the pot value
    """
    new_value = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.credits = 0

    def __iadd__(self, value):
        self.credits += value
        self.new_value.emit()

    def value(self):
        return self.credits

    def clear(self):
        """
        This method clears the pot
        """
        self.credits = 0
        self.new_value.emit()

    def update_pot(self):
        """
        This method calls to update pot view
        """
        self.new_value.emit()


class Player(Hand, QObject):
    """
    This is the player model that keeps tracks of the players logic
    """
    new_stack = pyqtSignal()
    new_activity = pyqtSignal()

    def __init__(self, name, stack, deck):
        Hand.__init__(self)
        QObject.__init__(self)
        self.name = name
        self.deck = deck
        self.stack = stack
        self.hand_model = HandModel()
        self.give_new_hand()
        self.current_bet = 0
        self.is_active = False

    def give_new_hand(self):
        """
        As the name suggests it gives the player a new hand
        """
        self.hand_model.add_card(self.deck.deal_card())
        self.hand_model.add_card(self.deck.deal_card())

    def update_stack(self, pot):
        """
        This method updates the stack for the player with credits from a pot
        :param pot: An integer with the amount won from the round
        :return: nothing but it changes the stack in the view
        """
        self.stack += pot
        self.new_stack.emit()

    def bet(self, amount):
        """
        This method takes the bet from the players stack
        :param amount: An integer that is equal to the amount of the bet
        :return: Nothing but it updates the stack in the view
        """
        self.stack -= amount
        self.new_stack.emit()

    def check_hand_strength(self, table_cards):
        """
        It gets a value of hand strength from the cardlib funktion for checking pokerhands
        :param table_cards: A list of cards from the table
        :return: The value that corresponds to the hand strength
        """
        return self.hand_model.best_poker_hand(table_cards)

    def change_activity(self, activity):
        """
        Sends a signal to change the view for the active/non active part of the player view
        :param activity: True or False depending on the player being the active player or not
        :return: Nothing but it does emit a signal to the playerview
        """
        self.is_active = activity
        self.new_activity.emit()


class PlayerState(QObject):
    """
    A class that represent all the player and total player states
    """
    turn_signal = pyqtSignal

    def __init__(self, deck):
        self.players = []
        self.players.append(Player('Lucas', 1000, deck))
        self.players.append(Player('Frida', 1000, deck))
        self.active_player = 0
        self.phase_check = 0
        self.turn_list = [0, 1]
        self.players[0].hand_model.flip()

    def check_winners(self, table_cards):
        """
        This method checks who the winner of a round is
        :param table_cards: A list of the cards on the table
        :return: It returns the index of the winning player
        """
        if self.players[0].check_hand_strength(table_cards) < self.players[1].check_hand_strength(table_cards):
            return 1
        elif self.players[0].check_hand_strength(table_cards) > self.players[1].check_hand_strength(table_cards):
            return 0
        elif self.players[0].check_hand_strength(table_cards) == self.players[1].check_hand_strength(table_cards):
            return 2


class GameState(QObject):
    """
    Gamestate is a class that keeps track of all the meta parts of the game logic
    """
    turn_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.table_hand = HandModel()
        self.table_hand.flip()
        self.pot = PotModel()
        self.game_phase = 0
        self.winning_player = None
        self.current_call_bet = 0
        self.turn_list = [0, 1]
        self.players = PlayerState(self.deck)
        self.activity()

        self.phase_check_extra = True

    def flopp(self):
        """
        This method deals the flop
        """
        if len(self.table_hand.cards) >= 3:
            return
        for i in range(0, 3):
            self.table_hand.add_card(self.deck.deal_card())

    def turn_river(self):
        """
        This method deals the river and turn
        """
        if len(self.table_hand.cards) >= 5:
            return
        self.table_hand.add_card(self.deck.deal_card())

    def new_phase(self):
        """
        This method checks for wich phase of the round the game is currently in and then deals cards/ends the round
        accordingly
        """
        if self.players.phase_check == 1:
            if self.game_phase == 0:
                self.flopp()
                self.game_phase += 1
                self.phase_check_extra = False

            elif self.game_phase == 1 or self.game_phase == 2:
                self.turn_river()
                self.game_phase += 1
                self.phase_check_extra = False

            else:
                self.new_round()
                self.phase_check_extra = False

            self.change_active_player(0)
        self.players.phase_check = 0
        self.activity()

    def fold(self):
        """
        This method makes the current player fold their hand
        """
        if self.players.active_player == 0:
            self.winning_player = 1
            self.new_round()

        elif self.players.active_player == 1:
            self.winning_player = 0
            self.new_round()

    def raise_bet(self, amount):
        """
        This method get called when the player bets and calls on the corresponding funktions to execute the correct
        logic
        :param amount: an integer that corresponds to the amount bet
        """
        temp_call_bet = amount
        amount += self.current_call_bet
        self.current_call_bet = temp_call_bet
        self.players.phase_check = 0

        if amount >= self.players.players[self.players.active_player].stack:
            amount = self.players.players[self.players.active_player].stack
        elif amount >= self.players.players[self.players.turn_list[1]].stack:
            amount = self.players.players[self.players.turn_list[1]].stack

        if amount == 0:
            self.check_or_call()

        else:
            self.current_call_bet = amount
            self.pot.credits += amount
            self.players.players[self.players.active_player].bet(amount)
            self.pot.update_pot()
            self.change_active_player()
            self.new_phase()
            self.players.phase_check = 1

    def check_or_call(self):
        """
        This method is called when a player either checks or calls, it executes the connected logic corresponding to
        it's event
        """
        self.pot.credits += self.current_call_bet
        self.players.players[self.players.active_player].bet(self.current_call_bet)
        self.pot.update_pot()
        self.current_call_bet = 0

        self.change_active_player()
        self.new_phase()  # TODO: problem: changes phase check after new phase
        if self.phase_check_extra:
            self.players.phase_check = 1

        self.phase_check_extra = True
        self.activity()

    def new_round(self):
        """
        This method creates a new round with a new deck and also tells the players who won the last round
        """
        self.winner()
        self.distribute_pot()
        self.deck = StandardDeck()
        self.table_hand.drop_all_cards()
        self.game_phase = 0
        self.players.phase_check = 0

        for player in self.players.players:
            player.deck = self.deck
            player.hand_model.drop_all_cards()
            player.give_new_hand()  # TODO Upppdatera vinnarens stack och byt starting_player

        if self.players.players[0].stack <= 0:
            self.player_won(1)
        elif self.players.players[1].stack <= 1:
            self.player_won(0)
        else:
            if self.winning_player == 2:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "The round ended in a tie")  # TODO: active player
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(
                    "The round winner is " + self.players.players[self.winning_player].name)  # TODO: active player
                msg.exec_()

    def distribute_pot(self):
        """
        This method distribute the pot to the winning player or makes a split pot if there's a tie
        """
        if self.winning_player == 2:
            self.players.players[0].update_stack(self.pot.credits/2)
            self.players.players[1].update_stack(self.pot.credits/2)
            self.pot.clear()
        else:
            self.players.players[self.winning_player].update_stack(self.pot.credits)
            self.pot.clear()

    def change_active_player(self, i=1):
        """
        This method changes the active player
        :param i: This is an integer that calls a special part of this method if there's a new phase and the active
        player should be the designated player to the left of the button
        """
        if i == 0:
            if self.players.active_player == 1:
                self.flip_player_cards()
            self.players.active_player = 0
            self.turn_list = [0, 1]

        elif self.players.active_player == 0:
            self.players.active_player = 1
            self.turn_list = [1, 0]
            self.flip_player_cards()

        elif self.players.active_player == 1:
            self.players.active_player = 0
            self.turn_list = [0, 1]
            self.flip_player_cards()
        self.activity()

    def winner(self):
        """
        This method calls to check which player won
        """
        self.winning_player = self.players.check_winners(self.table_hand.cards)

    def activity(self):
        """
        This method changes the players activity status
        """
        if self.turn_list == [0, 1]:
            self.players.players[0].change_activity(True)
            self.players.players[1].change_activity(False)

        elif self.turn_list == [1, 0]:
            self.players.players[1].change_activity(True)
            self.players.players[0].change_activity(False)

    def flip_player_cards(self):
        """
        This method calls on a method that flips the cards so that only the active players cards are shown
        """
        self.players.players[0].hand_model.flip()
        self.players.players[1].hand_model.flip()

    def player_won(self, index):
        """
        This method tells the players who won the game
        :param index: An integer that corresponds to who won the game
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("The winner of the game is: " + self.players.players[index].name +
                    '\n The other player ran out of money')  # TODO: active player
        msg.exec_()


class GameModel(QObject):
    """
    A simple class that initiates the game
    """
    def __init__(self):
        super().__init__()
        self.gamestate = GameState()


app = QApplication(sys.argv)
model = GameModel()
game = GameView(model)
game.show()
sys.exit(app.exec_())
