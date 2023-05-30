import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QColor, QFont
from Games.tic_tac_toe import TicTacToeGUI

class GameSelectionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('S2P -Game Selection')
        self.setFixedSize(300, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)

        tic_tac_toe_button = QPushButton('Tic Tac Toe')
        tic_tac_toe_button.setStyleSheet(
            '''
            QPushButton {
                background-color: #3CB371;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                color: #fff;
            }
            
            QPushButton:hover {
                background-color: #32CD32;
            }
            '''
        )
        tic_tac_toe_button.clicked.connect(self.open_tic_tac_toe)
        layout.addWidget(tic_tac_toe_button)

        checkers_button = QPushButton('Checkers')
        checkers_button.setStyleSheet(
            '''
            QPushButton {
                background-color: #FFA500;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                color: #fff;
            }
            
            QPushButton:hover {
                background-color: #FF8C00;
            }
            '''
        )
        checkers_button.clicked.connect(self.open_checkers)
        layout.addWidget(checkers_button)

        connect_4_button = QPushButton('Connect 4')
        connect_4_button.setStyleSheet(
            '''
            QPushButton {
                background-color: #4169E1;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                color: #fff;
            }
            
            QPushButton:hover {
                background-color: #0000CD;
            }
            '''
        )
        connect_4_button.clicked.connect(self.open_connect_4)
        layout.addWidget(connect_4_button)

        layout.addStretch()

        # Set a background color for the window
        self.setStyleSheet("background-color: #F5F5F5;")

    def open_tic_tac_toe(self):
        self.game = TicTacToeGUI()
        self.game.show()

    def open_checkers(self):
        self.hide()

    def open_connect_4(self):
        self.hide()

if __name__ == '__main__':
    app = QApplication([])
    window = GameSelectionGUI()
    window.show()
    sys.exit(app.exec())
