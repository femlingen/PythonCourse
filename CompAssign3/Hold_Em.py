from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from CompAssign3.cardlib import *
import sys
from CompAssign3.card_view import *

class Player(Hand):
    def __init__(self, player_name, player_stack):
        super().__init__()
        self.name = player_name
        self.stack = player_stack


# The QWidget class is the base class of all user interface objects.
# The widget is the atom of the user interface: it receives mouse, keyboard and
# other events from the window system, and paints a representation of itself on the screen.





class PlayerView(QGroupBox):

    def __init__(self, player): #TODO: Add dynamic player names and stacks
        super().__init__()
        self.namelabel = QLabel(player.name)
        self.stacklabel = QLabel(str(player.stack))
        # TODO: Add and also to layout self.playercards = CardView(player.hand)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.namelabel)
        self.layout.addWidget(self.stacklabel)
        self.setLayout(self.layout)
        # TODO: Add the player cards to layout self.layout.addWidget(self.playercards)


class TotalPlayerView(QGroupBox):

    def __init__(self, players):
        super().__init__()
        self.layout = QVBoxLayout()
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
        self.layout = QHBoxLayout(central)
        self.layout.addWidget(QLineEdit('0'))
        for button in buttons:
            self.layout.addWidget(button)


        self.slider = QSlider(Qt.Horizontal) # TODO: Remove or add (Depending on time)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)  # TODO: Add current player stack
        self.slider.setValue(0)
        self.setLayout(self.layout)



class BotView(QGroupBox):
    def __init__(self):
        super().__init__()
        players = []
        players.append(Player('Lucas', 1000))
        players.append(Player('Frida', 1000))
        player_views = TotalPlayerView(players)
        self.layout = QHBoxLayout()
        self.layout.addWidget(BetView())
        self.layout.addWidget(player_views)
        self.setLayout(self.layout)


class TopView(QGroupBox): # TODO: Fix all cards and pot added in this layout

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        table_cards = TableCardsView() # Fix tablecardsview



class GameView(QGroupBox):
    def __init__(self):  # TODO: Add game_model, game_players ?
        super().__init__()

        # self.players = players TODO: Add when players are back


        players_hbox = QHBoxLayout()



        #self.bg = QPixmap('Files/table.png')
        #self.setBackgroundBrush(QBrush(self.bg))

        raise_amount = 0

        self.setLayout(layout)



### Skapa en hand för bordet endast test
deck = StandardDeck()
deck.shuffle_cards()
table_hand = HandModel()
table_hand.add_card(deck.deal_card())
table_hand.add_card(deck.deal_card())
table_hand.add_card(deck.deal_card())
table_hand.add_card(deck.deal_card())
table_hand.add_card(deck.deal_card())
###

app = QApplication(sys.argv)

 # TODO: Add to main class instead
widget = QMainWindow()
central = QWidget()
widget.setCentralWidget(central)
botview = BotView()
vlayout = QVBoxLayout(central)
betview = BetView()
asd = TableCardsView(table_hand)
vlayout.addWidget(asd)
vlayout.addWidget(botview)

#widget.setGeometry(500, 500, 500, 500)
widget.show()

sys.exit(app.exec_())
# game = GameView()
