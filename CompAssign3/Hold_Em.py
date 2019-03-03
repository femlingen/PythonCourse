from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *


class Player(Hand):
    def __init__(self, player_name, player_stack):
        super().__init__()
        self.name = player_name
        self.stack = player_stack

# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.


class TableScene(QGraphicsScene):
    """ A TableScene class ...  """ # TODO
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('Files/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardSvgItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, id):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = id


class CardView(QGraphicsView):
    """ A CardView class ... """ # TODO
    def __read_cards():
        all_cards = dict()
        for suit in 'HDSC':
            for value in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
                file = value + suit
                all_cards[file] = QSvgRenderer('Files/cards/' + file + '.svg')
        return all_cards
    back_card = QSvgRenderer('Files/cards/Red_Back.svg')
    all_cards = __read_cards()


class GameView(QWidget):
    def __init__(self):  # TODO: Add game_model, game_players ?
        super().__init__(self)
        layout = QVBoxLayout() # yttersta boxen
        first_vbox = QHBoxLayout() # översta boen
        second_vbox = QHBoxLayout() # understa
        layout.addLayout(first_vbox)
        layout.addLayout(second_vbox)

        players_hbox = QHBoxLayout()
        player_name_labels = [QLabel('Spelare 1'), QLabel('Spelare 2')] # TODO: Add dynamic player names
        player_stack_labels = [QLabel(1000), QLabel(1000)] # TODO: Add dynamic stacks
        players_hbox.addWidget()

        self.bg = QPixmap('Files/table.png')
        self.setBackgroundBrush(QBrush(self.bg))

        raise_amount = 0
        #self.players = players TODO: Add when players are back

        self.buttons = [QPushButton('Raise'), QPushButton('Check/Fold'), QPushButton('Fold')]

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000) # TODO: Add current player stack
        self.slider.setValue(0)


player1 = Player('Frida', 1000)
player2 = Player('Lucas', 1000)

app = QApplication([])
table_scene = TableScene()

content = QWidget()
#table_scene.addWidget(content)
table_scene.addEllipse(10,10,10,10)

okbutton = QPushButton("OK")
cbutton = QPushButton("Cancel")

hbox = QHBoxLayout()
hbox.addWidget(okbutton)
hbox.addWidget(cbutton)

content.setLayout(hbox)
#content.setGeometry(300, 300, 300, 300)


view = QGraphicsView(table_scene)
view.show()


# layout = QHBoxLayout()


# button = QPushButton("Klicka på mig")
# layout.addWidget(button)
# layout.addWidget(QLabel("Test"))
# #table_scene.addWidget(button)
# #table_scene.addText("Welcome to our pokergame")
#
#
# gameView = QGraphicsView(table_scene)
# gameView.show()


# window.setLayout(layout)
# window.show()
app.exec()


# game = GameView()
