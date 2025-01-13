# main.py
import sys
from PyQt5.QtWidgets import QApplication
from game import SnakeGame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec_())
