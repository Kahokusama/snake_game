# game.py
import sys
import random
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from settings import *

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("貪食蛇遊戲")
        self.setGeometry(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setStyleSheet("background-color: #2E2E2E;")
        
        # 遊戲變數
        self.snake_body = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = 'RIGHT'
        self.food_position = (random.randrange(1, (SCREEN_WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                              random.randrange(1, (SCREEN_HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE)
        self.food_spawn = True
        self.score = 0

        # 設定定時器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(SNAKE_SPEED)

    def update_game(self):
        self.move_snake()
        self.check_collision()
        self.check_food_collision()
        self.spawn_food()
        self.update()

    def move_snake(self):
        head_x, head_y = self.snake_body[0]
        if self.snake_direction == 'UP':
            head_y -= SNAKE_SIZE
        if self.snake_direction == 'DOWN':
            head_y += SNAKE_SIZE
        if self.snake_direction == 'LEFT':
            head_x -= SNAKE_SIZE
        if self.snake_direction == 'RIGHT':
            head_x += SNAKE_SIZE

        new_head = (head_x, head_y)
        self.snake_body = [new_head] + self.snake_body[:-1]

    def check_collision(self):
        head_x, head_y = self.snake_body[0]

        # 碰到牆壁
        if head_x >= SCREEN_WIDTH or head_x < 0 or head_y >= SCREEN_HEIGHT or head_y < 0:
            self.game_over()

        # 碰到自己
        if (head_x, head_y) in self.snake_body[1:]:
            self.game_over()

    def check_food_collision(self):
        head_x, head_y = self.snake_body[0]
        if (head_x, head_y) == self.food_position:
            self.food_spawn = False
            self.score += 10
            self.snake_body.append(self.snake_body[-1])

    def spawn_food(self):
        if not self.food_spawn:
            self.food_position = (random.randrange(1, (SCREEN_WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                                  random.randrange(1, (SCREEN_HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE)
            self.food_spawn = True

    def game_over(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"遊戲結束! 您的分數是: {self.score}")
        msg.setWindowTitle("遊戲結束")
        msg.exec_()

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left and self.snake_direction != 'RIGHT':
            self.snake_direction = 'LEFT'
        elif event.key() == Qt.Key_Right and self.snake_direction != 'LEFT':
            self.snake_direction = 'RIGHT'
        elif event.key() == Qt.Key_Up and self.snake_direction != 'DOWN':
            self.snake_direction = 'UP'
        elif event.key() == Qt.Key_Down and self.snake_direction != 'UP':
            self.snake_direction = 'DOWN'

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 繪製蛇
        painter.setBrush(QColor(*GREEN))
        for segment in self.snake_body:
            painter.drawRect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)

        # 繪製食物
        painter.setBrush(QColor(*RED))
        painter.drawRect(self.food_position[0], self.food_position[1], SNAKE_SIZE, SNAKE_SIZE)

        # 繪製分數
        painter.setPen(QColor(*WHITE))
        painter.setFont(QFont(FONT_STYLE, FONT_SIZE))
        painter.drawText(10, 30, f"分數: {self.score}")
