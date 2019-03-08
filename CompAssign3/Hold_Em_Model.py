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

    def increment(self):
        self.credits += 1
        self.new_value.emit()

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

    def __init__(self, gamestate):
        super().__init__()
        self.gamestate = gamestate

    def fold(self):
        for player in self.gamestate.playermodel.players:
            if player.active_player == False:
                # TODO: tilldela pot
                pass
        self.bet_signal.emit()

    def raise_bet(self):
        # TODO: horisontal slider with min value = 0 and max value player.stack
        # raise
        # change active player
        pass

    def check_or_call(self):

        # change stack amount om man callar
        # change active player
        pass


class Player(Hand):
    def __init__(self, player_name, player_stack, deck):
        super().__init__()
        self.name = player_name
        self.stack = player_stack
        self.active_player = False
        self.hand_model = HandModel()
        self.hand_model.add_card(deck.deal_card())
        self.hand_model.add_card(deck.deal_card())


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class PlayerState(QObject):
    def __init__(self, deck):
        self.players = []
        self.players.append(Player('Lucas', 1000, deck))
        self.players.append(Player('Frida', 1000, deck))


class GameState(QObject):
    def __init__(self):
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        self.table_hand = HandModel()
        self.pot = PotModel()
        for i in range(0, 5):
            self.table_hand.add_card(self.deck.deal_card())

    def restart_game(self):
        pass
        # do shit
        # kallar på spelare - nya kort
        # kallar på bordet - nya kort
        # emit-funktion som uppdaterar game view


# metod  playmessage (str)
# messagebox som målar upp messagebox
# lyssnar på gamemessage-signal som initieras av metamodellen

class GameModel(QObject):
    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        self.playermodel = PlayerState(self.deck)
        self.gamestate = GameState()
        self.tablelayout = TopView(self.gamestate.table_hand, self.gamestate.pot)
        self.playerlayout = BottomView(self.playermodel.players)


app = QApplication(sys.argv)
model = GameModel()
game = GameView(model)
game.show()
sys.exit(app.exec_())
