from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
import sys
from CompAssign3.card_view import *
from CompAssign3.Hold_Em_View import *


class PotModel(QObject):
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
        self.credits = 0
        self.new_value.emit()

    def update_pot(self):
        self.new_value.emit()


class BetModel(QObject):
    bet_signal = pyqtSignal()

    def __init__(self):  # TODO Skall denna klassen behöva ta in gamestate? Nu lägger vi allt längre "ut" i processen
        super().__init__()


class Player(Hand, QObject):
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
        self.hand_model.add_card(self.deck.deal_card())
        self.hand_model.add_card(self.deck.deal_card())

    def update_stack(self, pot):
        self.stack += pot
        self.new_stack.emit()

    def bet(self, amount):
        self.stack -= amount
        self.new_stack.emit()

    def check_hand_strength(self, table_cards):
        return self.hand_model.best_poker_hand(table_cards)

    def change_activity(self, activity):
        self.is_active = activity
        self.new_activity.emit()

# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class PlayerState(QObject):
    turn_signal = pyqtSignal

    def __init__(self, deck):
        self.players = []
        self.players.append(Player('Lucas', 1000, deck))
        self.players.append(Player('Frida', 1000, deck))
        self.active_player = 0
        self.phase_check = 0
        self.turn_list = [0, 1]

    def check_winners(self, table_cards):
        if self.players[0].check_hand_strength(table_cards) < self.players[1].check_hand_strength(table_cards):
            return 0
        elif self.players[0].check_hand_strength(table_cards) > self.players[1].check_hand_strength(table_cards):
            return 1
        elif self.players[0].check_hand_strength(table_cards) == self.players[1].check_hand_strength(table_cards):
            return 2


class GameState(QObject):
    turn_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.table_hand = HandModel()
        self.pot = PotModel()
        self.bet_model = BetModel()
        self.game_phase = 0
        self.winning_player = None
        self.current_call_bet = 0
        self.turn_list = [0, 1]
        self.players = PlayerState(self.deck)
        self.activity()

    def flopp(self):
        if len(self.table_hand.cards) >= 3:
            return
        for i in range(0, 3):
            self.table_hand.add_card(self.deck.deal_card())

    def turn_river(self):
        if len(self.table_hand.cards) >= 5:
            return
        self.table_hand.add_card(self.deck.deal_card())

    def new_phase(self):
        if self.players.phase_check == 1:
            if self.game_phase == 0:
                self.flopp()
                self.game_phase += 1

            elif self.game_phase == 1 or self.game_phase == 2:
                self.turn_river()
                self.game_phase += 1

            else:
                self.new_round()

            self.change_active_player(0)
        self.players.phase_check = 0
        self.activity()

    def fold(self):

        if self.players.active_player == 0:
            self.winning_player = 1
            self.new_round()

        elif self.players.active_player == 1:
            self.winning_player = 0
            self.new_round()

    def raise_bet(self, amount):
        temp_call_bet = amount
        amount += self.current_call_bet
        self.current_call_bet = temp_call_bet
        self.players.phase_check = 0

        if amount >= self.players.players[self.players.active_player].stack:
            amount = self.players.players[self.players.active_player].stack

        if amount == 0:
            self.check_or_call()

        else:
            self.pot.credits += amount
            self.players.players[self.players.active_player].bet(amount)
            self.pot.update_pot()
            self.change_active_player()
            self.new_phase()
            self.players.phase_check = 1


    def check_or_call(self):

        self.pot.credits += self.current_call_bet
        self.players.players[self.players.active_player].bet(self.current_call_bet)
        self.pot.update_pot()
        self.current_call_bet = 0

        self.change_active_player()
        self.new_phase()
        self.players.phase_check = 1
        self.activity()

    def new_round(self):
        self.distribute_pot()
        self.deck = StandardDeck()
        self.table_hand.drop_all_cards()
        self.game_phase = 0
        self.players.phase_check = 0

        for player in self.players.players:
            player.deck = self.deck
            player.hand_model.drop_all_cards()
            player.give_new_hand()  # TODO Upppdatera vinnarens stack och byt starting_player
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("The winner is " + self.players.players[self.winning_player].name)  # TODO: active player
        msg.exec_()

    def distribute_pot(self):
        if self.winner() == 2:
            self.players.players[0].update_stack(self.pot.credits/2)
            self.players.players[1].update_stack(self.pot.credits/2)
            self.pot.clear()
        else:
            self.players.players[self.winning_player].update_stack(self.pot.credits)
            self.pot.clear()

    def change_active_player(self, i=1):
        if i == 0:
            self.players.active_player = 1
            self.turn_list = [0,1]

        if self.players.active_player == 0:
            self.players.active_player = 1
            self.turn_list = [1, 0]
        elif self.players.active_player == 1:
            self.players.active_player = 0
            self.turn_list = [0, 1]
        self.activity()

    def winner(self):
        self.winning_player = self.players.check_winners(self.table_hand.cards)

    def activity(self):
        if self.turn_list == [0, 1]:
            self.players.players[0].change_activity(True)
            self.players.players[1].change_activity(False)

        elif self.turn_list == [1, 0]:
            self.players.players[1].change_activity(True)
            self.players.players[0].change_activity(False)


# metod  playmessage (str)
# messagebox som målar upp messagebox
# lyssnar på gamemessage-signal som initieras av metamodellen


class GameModel(QObject):
    def __init__(self):
        super().__init__()
        self.start_game()

    def start_game(self):
        self.gamestate = GameState()


app = QApplication(sys.argv)
model = GameModel()
game = GameView(model)
game.show()
sys.exit(app.exec_())
