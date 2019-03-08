from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
from CompAssign3.card_view import *


class Player(Hand):
    def __init__(self, player_name, player_stack):
        super().__init__()
        self.name = player_name
        self.stack = player_stack

    def get_stack(self):
        return self.stack

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
        first_vbox = QHBoxLayout()
        second_vbox = QHBoxLayout()
        layout.addLayout(first_vbox)
        layout.addLayout(second_vbox)

        players_hbox = QHBoxLayout()
        player_name_labels = [QLabel(player1.name), QLabel(player2.name)] # TODO: Add dynamic player names
        player_stack_labels = [QLabel(player1.stack), QLabel(player2.stack)] # TODO: Add dynamic stacks
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




# MAYBE REMOVE Potmodel and Texasholdemmodel
class PotModel:
    new_value = pyqtSignal()

    def __init__():
        self.credits = 0

    def __iadd__(self, value):
        self.credits += value
        self.new_value.emit()

    def value(self):
        return self._credits()

    def clear(self):
        self.credits = 0
        self.new_value.emit()

    def pot_view(QLabel):
        def __init__(self, pot: PotModel):
            self.pot = pot
            self.pot.new: value.connect(lambda: self.setText('S()'.format(self.pot.value())))

        def update_value(self):
            self.setText('S()'.format(self.pot.value()))


class TexasHoldEmModel:

    def __init__(self, player_names, starting_credits = 100):
        self.players = [Player(name, starting_credits) for name in player_names]
        self.pot = PotModel()

    def place_bet(self, amount):
        self.players[self.active_player].place_bet(amount)  # this subtracts fom the players credits
        self.pot += amount

    def fold(self):
        next_player = (self.active_player + 1 % len(self.players))
        self.players[next_player].win(self.pot.value())
        self.next_round()  # probably clear the deck, the player cards and create a new deck.


    #def next_round():  # any sort of clean up we need here
        #self.deck = StandardDeck()
        #self.pot.clear()

        #self.active_player = (self_player)
        #self.new_active_player.emit()  # always call for emit-signal


# TODO: Potmodel
# TODO: playermodel
# TODO: handmodel
# TODO: tablemodel
# TODO: playerview
# TODO: game board view
# TODO: restart function

player1 = Player('Frida', 1000)
player2 = Player('Lucas', 1000)

app = QApplication([])
table_scene = TableScene()

content = QWidget()
table_scene.addWidget(content)

# Button
cancel_button = QPushButton("End Game")
fold_button = QPushButton("Fold")
check_button = QPushButton("Check")
check_fold_button = QPushButton("Check/fold")
call_any_button = QPushButton("Call Any")
raise_button = QPushButton("Raise")


# Card section
table_cards_hbox = QHBoxLayout()
table_cards_hbox.addWidget(QLabel("Card"))

# Button section
button_hbox = QHBoxLayout()
button_hbox.addWidget(fold_button)
button_hbox.addWidget(check_button)
button_hbox.addWidget(check_fold_button)
button_hbox.addWidget(call_any_button)
button_hbox.addWidget(raise_button)
button_hbox.addWidget(cancel_button)


content.setLayout(button_hbox)
#content.setGeometry(300, 300, 300, 300)


view = QGraphicsView(table_scene)
view.show()


app.exec()


# game = GameView()


# Kör en gameview som innehåller komponenter så som
# PlayerView
# TableCardView
# Button panel
# GameModel