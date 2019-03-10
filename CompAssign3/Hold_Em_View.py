from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
from PyQt5 import QtSvg
import sys
from PyQt5 import QtWidgets, QtGui,QtCore
from CompAssign3.card_view import *


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class TopView(QGroupBox):  # TODO: Fix all cards and pot added in this layout

    def __init__(self, model):
        super().__init__()
        self.layout = QHBoxLayout()
        self.model = model
        self.table_cards = TableCardsView(self.model.gamestate.table_hand)  # Fix tablecardsview
        self.pot_view = PotView(self.model.gamestate.pot)
        self.layout.addWidget(self.table_cards)
        self.layout.addWidget(self.pot_view)
        self.setLayout(self.layout)


class BetView(QGroupBox):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.buttons = [QPushButton('Raise'), QPushButton('Call/Check'), QPushButton('Fold')]
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLineEdit('0'))
        for button in self.buttons:
            self.layout.addWidget(button)
            button.setStyleSheet("QPushButton { background-color: white; border-style: outset; border-width: 2px; "
                                 "border-radius: 10px; border-color: beige; "
                                 "font: bold 14px; "
                                 "min-width: 10em; "
                                 "padding: 6px; }"
                                 "QPushButton:pressed { background-color: green }" )

        self.buttons[0].clicked.connect(self.model.new_phase) # TODO Ändra till bet_model.raise_bet istället för att lägga tiill kort
        self.buttons[1].clicked.connect(self.model.new_phase)  # TODO Som ovan fast till check_or_call
        self.buttons[2].clicked.connect(self.model.fold)  # TODO Som ovan fast med fold (bet_model.fold)

        self.slider = QSlider(Qt.Horizontal)  # TODO: Remove or add (Depending on time)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)  # TODO: Add current player stack
        self.slider.setValue(0)

        self.setLayout(self.layout)


class BottomView(QGroupBox):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.player_views = TotalPlayerView(self.model.players)
        self.layout = QHBoxLayout()
        self.layout.addWidget(BetView(self.model))
        self.layout.addWidget(self.player_views)
        self.setLayout(self.layout)


class PlayerView(QGroupBox):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.v_layout = QVBoxLayout()

        self.name_label = QLabel(self.player.name)
        self.stack_label = QLabel(str(self.player.stack))

        is_active = True

        if is_active:  # TODO: change to the variable is active
            active_label = QLabel("Your turn")
            self.v_layout.addWidget(active_label)
            self.setStyleSheet(" QWidget { font: bold 24px; background-color: #5AD48F; }")

        self.v_layout.addWidget(self.name_label)
        self.v_layout.addWidget(self.stack_label)

        self.name_label.setFont(QtGui.QFont('SansSerif', 24))
        self.stack_label.setFont(QtGui.QFont('SansSerif', 16))

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.v_layout)
        self.layout.addWidget(CardView(self.player.hand_model))

        self.setStyleSheet(" CardView { min-width: 14em; max-width: 20em; max-height: 12em; }")
        self.setLayout(self.layout)

        self.player.new_stack.connect(self.update_value)
        self.update_value()

    def update_value(self):
        self.stack_label.setText('Stack:\n${}'.format(self.player.stack))


class TotalPlayerView(QGroupBox):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QHBoxLayout()
        for player in self.model.players:
            self.layout.addWidget(PlayerView(player))
        self.setStyleSheet("QLabel { padding: 2px; }")
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

        self.pot_label.setFont(QtGui.QFont('SansSerif', 18))
        self.pot_label.setStyleSheet("QLabel { padding: 6px; min-width: 5em; }")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.pot_label)
        self.setLayout(self.layout)

        self.update_value()
        self.pot.new_value.connect(self.update_value)

    def update_value(self):
        self.pot_label.setText('Pot ${}'.format(self.pot.value()))


class GameView(QWidget):
    def __init__(self, total_model):
        super().__init__()
        self.widget = QMainWindow()
        self.central = QWidget()
        self.widget.setCentralWidget(self.central)
        self.game_model = total_model
        self.tablelayout = TopView(self.game_model)
        self.playerlayout = BottomView(self.game_model.gamestate)
        self.vlayout = QVBoxLayout(self.central)
        self.vlayout.addWidget(self.tablelayout)
        self.vlayout.addWidget(self.playerlayout)
        self.setLayout(self.vlayout)
        self.styleSheet()
        self.width = 700
        self.height = 450
        self.setGeometry(150, 150, self.width, self.height)
        self.setWindowTitle("Texas HoldEm")
        self.show()



