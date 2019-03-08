from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
import sys
from CompAssign3.card_view import *


class Player(Hand):
    def __init__(self, player_name, player_stack, deck):
        super().__init__()
        self.name = player_name
        self.stack = player_stack
        self.hand_model = HandModel()
        self.hand_model.add_card(deck.deal_card())
        self.hand_model.add_card(deck.deal_card())


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class PlayerView(QGroupBox):

    def __init__(self, player):  # TODO: Add dynamic player names and stacks
        super().__init__()
        self.namelabel = QLabel(player.name)
        self.stacklabel = QLabel(str(player.stack))
        # TODO: Add and also to layout self.playercards = CardView(player.hand)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.namelabel)
        self.layout.addWidget(self.stacklabel)
        self.layout.addWidget(CardView(player.hand_model))
        self.setLayout(self.layout)
        # TODO: Add the player cards to layout self.layout.addWidget(self.playercards)


class TotalPlayerView(QGroupBox):

    def __init__(self, players):
        super().__init__()
        self.layout = QHBoxLayout()
        for player in players:
            self.layout.addWidget(PlayerView(player))
        self.setLayout(self.layout)


class TableCardsView(QGroupBox):
    def __init__(self, table_hand: Hand):
        super().__init__()

        box = QVBoxLayout()
        card_view = CardView(table_hand)
        self.layout = QHBoxLayout()
        self.layout.addWidget(card_view)
        self.setLayout(self.layout)


class BetView(QGroupBox):
    def __init__(self):
        super().__init__()
        buttons = [QPushButton('Raise'), QPushButton('Call/Check'), QPushButton('Fold')]
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLineEdit('0'))
        for button in buttons:
            self.layout.addWidget(button)

        self.slider = QSlider(Qt.Horizontal)  # TODO: Remove or add (Depending on time)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)  # TODO: Add current player stack
        self.slider.setValue(0)
        self.setLayout(self.layout)


class BotView(QGroupBox):
    def __init__(self, players):
        super().__init__()
        player_views = TotalPlayerView(players)
        self.layout = QHBoxLayout()
        self.layout.addWidget(BetView())
        self.layout.addWidget(player_views)
        self.setLayout(self.layout)


class TopView(QGroupBox):  # TODO: Fix all cards and pot added in this layout

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        table_cards = TableCardsView()  # Fix tablecardsview

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
        self.pot = 0
        for i in range(0, 5):
            self.table_hand.add_card(self.deck.deal_card())




class GameModell(QObject):

    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        self.playermodel = PlayerState(self.deck)
        self.gamestate = GameState()
        self.tablelayout = TableCardsView(self.gamestate.table_hand)
        self.playerlayout = BotView(self.playermodel.players)



class GameView(QWidget):
    def __init__(self):  # TODO: Add game_model, game_players ?
        super().__init__()
        self.widget = QMainWindow()
        self.central = QWidget()
        self.widget.setCentralWidget(self.central)
        self.game_modell = GameModell()
        self.vlayout = QVBoxLayout(self.central)
        self.vlayout.addWidget(self.game_modell.tablelayout)
        self.vlayout.addWidget(self.game_modell.playerlayout)
        self.setLayout(self.vlayout)
        self.show()




app = QApplication(sys.argv)
game = GameView()
# TODO: Add to main class instead
# # widget = QMainWindow()
# central = QWidget()
# widget.setCentralWidget(central)
# #botview = BotView()
# vlayout = QVBoxLayout(central)
# betview = BetView()
# asd = TableCardsView(table_hand)
# vlayout.addWidget(asd)
# vlayout.addWidget(botview)

# widget.setGeometry(500, 500, 500, 500)
#widget.show()

sys.exit(app.exec_())
# game = GameView()
