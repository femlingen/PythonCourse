from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
import sys
from CompAssign3.card_view import *


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class TopView(QGroupBox):  # TODO: Fix all cards and pot added in this layout

    def __init__(self, table_hand, pot):
        super().__init__()
        self.layout = QHBoxLayout()
        table_cards = TableCardsView(table_hand)  # Fix tablecardsview
        pot_view = PotView(pot)
        self.layout.addWidget(table_cards)
        self.layout.addWidget(pot_view)
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


class BottomView(QGroupBox):
    def __init__(self, players):
        super().__init__()
        player_views = TotalPlayerView(players)
        self.layout = QHBoxLayout()
        self.layout.addWidget(BetView())
        self.layout.addWidget(player_views)
        self.setLayout(self.layout)


class PlayerView(QGroupBox):
    def __init__(self, player):
        super().__init__()
        self.namelabel = QLabel(player.name) # TODO: hitta något sätt att ändra stacken på
        self.stacklabel = QLabel(str(player.stack))
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.namelabel)
        self.layout.addWidget(self.stacklabel)
        self.layout.addWidget(CardView(player.hand_model))
        self.setLayout(self.layout)


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
        card_view = CardView(table_hand)
        self.layout = QHBoxLayout()
        self.layout.addWidget(card_view)
        self.setLayout(self.layout)


class PotView(QGroupBox):

    def __init__(self, pot_model):
        super().__init__()
        self.pot = pot_model
        self.pot_label = QLabel(str(self.pot.value()))

        self.button = QPushButton("Test: +1")
        self.button.clicked.connect(self.pot.increment)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.pot_label)
        self.setLayout(self.layout)

        self.update_value()
        self.pot.new_value.connect(self.update_value)

    def update_value(self):
        self.pot_label.setText('Pot value ${}'.format(self.pot.value()))


class GameView(QWidget):
    def __init__(self, model):  # TODO: Add game_model, game_players ?
        super().__init__()
        self.widget = QMainWindow()
        self.central = QWidget()
        self.widget.setCentralWidget(self.central)
        self.game_model = model
        self.vlayout = QVBoxLayout(self.central)
        self.vlayout.addWidget(self.game_model.tablelayout)
        self.vlayout.addWidget(self.game_model.playerlayout)
        self.setLayout(self.vlayout)
        self.show()



