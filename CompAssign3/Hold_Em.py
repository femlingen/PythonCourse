from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from cardlib import *
import sys


class Player(Hand):
    def __init__(self, player_name, player_stack):
        super().__init__()
        self.name = player_name
        self.stack = player_stack


class GameView(QWidget):
    def __init__(self): # TODO: Add game_model, game_players ?
        #super().__init__(self)
        layout = QHBoxLayout()
        first_vbox = QVBoxLayout()
        second_vbox = QVBoxLayout()
        layout.addLayout(first_vbox)
        layout.addLayout(second_vbox)

        players_hbox = QHBoxLayout()
        player_name_labels = [QLabel('Spelare 1'), QLabel('Spelare 2')] # TODO: Add dynamic player names
        player_stack_labels = [QLabel(1000), QLabel(1000)] # TODO: Add dynamic stacks
        players_hbox.addWidget()


        self.bg = QPixmap('Files/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


        raise_ammount = 0
        #self.players = players TODO: Add when players are back

        self.buttons = [QPushButton('Raise'), QPushButton('Check/Call'), QPushButton('Fold')]


        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000) # TODO: Add current player stack
        self.slider.setValue(0)
        layout.addStretch(1)
        self.setLayout(layout)
        self.show()




class CardSvgItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, id):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = id



player1 = Player('Frida', 1000)
player2 = Player('Lucas', 1000)

game = GameView()
game_app.exec_()