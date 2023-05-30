import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QLabel, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# Create a 3x3 game board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Create the GUI window
class TicTacToeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tic Tac Toe')
        self.setGeometry(100, 100, 300, 400)

        # Create buttons for each cell on the board
        self.buttons = []
        layout = QGridLayout()

        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton('', self)
                button.setFixedSize(90, 90)
                button.setStyleSheet("QPushButton { background-color: #e8e8e8; color: #333333; font-size: 24px; }"
                                     "QPushButton:pressed { background-color: #cccccc; }"
                                     "QPushButton:disabled { background-color: #e8e8e8; color: #999999; }")
                button.clicked.connect(lambda _, i=i, j=j: self.buttonClicked(i, j))
                layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        # Create labels for displaying game status
        self.status_label = QLabel('', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 14))
        layout.addWidget(self.status_label, 3, 0, 1, 3)

        # Create the Start button
        start_button = QPushButton('Start', self)
        start_button.setFont(QFont('Arial', 12))
        start_button.clicked.connect(self.startClicked)
        layout.addWidget(start_button, 4, 0, 1, 3)

        # Create the Restart button
        restart_button = QPushButton('Restart', self)
        restart_button.setFont(QFont('Arial', 12))
        restart_button.clicked.connect(self.restartClicked)
        layout.addWidget(restart_button, 5, 0, 1, 3)

        # Create the difficulty level selector
        difficulty_label = QLabel('Difficulty:', self)
        difficulty_label.setFont(QFont('Arial', 12))
        layout.addWidget(difficulty_label, 6, 0, 1, 1)

        self.difficulty_combo = QComboBox(self)
        self.difficulty_combo.setFont(QFont('Arial', 12))
        self.difficulty_combo.addItem('Easy')
        self.difficulty_combo.addItem('Medium')
        self.difficulty_combo.addItem('Hard')
        layout.addWidget(self.difficulty_combo, 6, 1, 1, 2)

        self.setLayout(layout)
        self.show()

    def buttonClicked(self, row, col):
        # Handle button click event
        if board[row][col] == ' ':
            # Make the human player move
            make_move(row, col, 'X')
            self.buttons[row][col].setText('X')
            self.buttons[row][col].setEnabled(False)

            # Check if the game is over
            if is_game_over():
                self.updateStatus()
                show_message('Game Over')

                # Disable all buttons after the game is over
                self.disableButtons()
            elif is_game_tie():
                self.updateStatus()
                show_message('It\'s a draw!')

                # Disable all buttons after the game is over
                self.disableButtons()
            else:
                # Make the AI player move
                difficulty = self.difficulty_combo.currentText()
                if difficulty == 'Easy':
                    self.random_move()
                elif difficulty == 'Medium':
                    self.minimax_move()
                else:
                    self.alphabeta_move()

                # Check if the game is over again
                if is_game_over():
                    self.updateStatus()
                    show_message('Game Over')

                    # Disable all buttons after the game is over
                    self.disableButtons()
                elif is_game_tie():
                    self.updateStatus()
                    show_message('It\'s a draw!')

                    # Disable all buttons after the game is over
                    self.disableButtons()

    def startClicked(self):
        # Start the game
        self.enableButtons()
        self.clearLabels()

    def restartClicked(self):
        # Restart the game
        reset_game()
        self.enableButtons()
        self.clearLabels()
        self.status_label.setText('')

    def random_move(self):
        import random
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        if available_moves:
            row, col = random.choice(available_moves)
            make_move(row, col, 'O')
            self.buttons[row][col].setText('O')
            self.buttons[row][col].setEnabled(False)

    def minimax_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = self.minimax(board, False)
                    board[i][j] = ' '

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        row, col = best_move
        make_move(row, col, 'O')
        self.buttons[row][col].setText('O')
        self.buttons[row][col].setEnabled(False)

    def alphabeta_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = self.alphabeta(board, float('-inf'), float('inf'), False)
                    board[i][j] = ' '

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        row, col = best_move
        make_move(row, col, 'O')
        self.buttons[row][col].setText('O')
        self.buttons[row][col].setEnabled(False)

    def minimax(self, board, is_maximizing):
        if is_game_over():
            if is_maximizing:
                return -1  # Human wins
            else:
                return 1  # AI wins
        elif is_game_tie():
            return 0  # Draw

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def alphabeta(self, board, alpha, beta, is_maximizing):
        if is_game_over():
            if is_maximizing:
                return -1  # Human wins
            else:
                return 1  # AI wins
        elif is_game_tie():
            return 0  # Draw

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.alphabeta(board, alpha, beta, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if alpha >= beta:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.alphabeta(board, alpha, beta, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if alpha >= beta:
                            break
            return best_score

    def updateStatus(self):
        if is_game_over():
            self.status_label.setText('Game Over')
        elif is_game_tie():
            self.status_label.setText('It\'s a draw!')
        else:
            self.status_label.setText('')

    def disableButtons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def enableButtons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)

    def clearLabels(self):
        for row in self.buttons:
            for button in row:
                button.setText('')

# Helper function to show a message box
def show_message(message):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.exec()

# Helper function to check if the game is over
def is_game_over():
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True

    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ' or board[0][2] == board[1][1] == board[2][0] != ' ':
        return True

    return False

# Helper function to check if the game is a tie
def is_game_tie():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Helper function to make a move
def make_move(row, col, player):
    board[row][col] = player

# Helper function to reset the game
def reset_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = TicTacToeGUI()
    sys.exit(app.exec_())
