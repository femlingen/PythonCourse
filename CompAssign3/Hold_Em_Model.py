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


class BetModel(QObject):
    bet_signal = pyqtSignal()

    def __init__(self):  # TODO Skall denna klassen behöva ta in gamestate? Nu lägger vi allt längre "ut" i processen
        super().__init__()


class Player(Hand, QObject):
    new_stack = pyqtSignal()

    def __init__(self, name, stack, deck):
        Hand.__init__(self)
        QObject.__init__(self)
        self.name = name
        self.deck = deck
        self.stack = stack
        self.active_player = False
        self.hand_model = HandModel()
        self.give_new_hand()
        self.current_bet = 0

    def give_new_hand(self):
        self.hand_model.add_card(self.deck.deal_card())
        self.hand_model.add_card(self.deck.deal_card())

    def update_stack(self, pot):
        self.stack += pot
        self.new_stack.emit()


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class PlayerState(QObject):
    def __init__(self, deck):
        self.players = []
        self.players.append(Player('Lucas', 1000, deck))
        self.players.append(Player('Frida', 1000, deck))
        self.active_player = 0
        self.phase_check = 0


class GameState(QObject):
    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.table_hand = HandModel()
        self.pot = PotModel()
        self.bet_model = BetModel()
        self.game_phase = 0
        self.winning_player = None

        self.players = PlayerState(self.deck)

    def flopp(self):
        if len(self.table_hand.cards) >= 3:
            # TODO logic if raising
            return
        for i in range(0, 3):
            self.table_hand.add_card(self.deck.deal_card())

    def turn_river(self):
        if len(self.table_hand.cards) >= 5:
            # TODO logic if turn river?

            return
        self.table_hand.add_card(self.deck.deal_card())

    def new_phase(self): #TODO när båda har call = true så kallar vi på new phase
        if self.game_phase == 0:
            self.flopp()
            self.game_phase += 1

        elif self.game_phase == 1 or self.game_phase == 2:
            self.turn_river()
            self.game_phase += 1

        else:
            self.new_round()

    def fold(self):

        if self.players.active_player == 0:
            self.winning_player = 1
            self.new_round()

        elif self.players.active_player == 1:
            self.winning_player = 0
            self.new_round()

    def raise_bet(self):
        # TODO: horisontal slider with min value = 0 and max value player.stack
        # raise
        # change active player
        pass

    def check_or_call(self):
        self.players.phase_check +=1

        if self.players.phase_check == 2:
            self.new_phase()
            # change stack amount om man callar
            # change active player

    def new_round(self):
        self.distribute_pot()
        self.deck = StandardDeck()
        self.table_hand.drop_all_cards()
        self.game_phase = 0

        for player in self.players.players:
            player.deck = self.deck
            player.hand_model.drop_all_cards()
            player.give_new_hand()  # TODO Upppdatera vinnarens stack och byt starting_player
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("The winner is " + self.players.players[self.winning_player].name)  # TODO: active player
        msg.exec_()

    def distribute_pot(self):
        self.players.players[self.winning_player].update_stack(self.pot.credits)
        self.pot.clear()

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
