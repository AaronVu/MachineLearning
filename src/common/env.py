# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtWidgets import QVBoxLayout
import numpy as np
import random
import sys
import time


class MazeEnv(QtWidgets.QWidget):

    def __init__(self, rows=5, cols=5):
        super(MazeEnv, self).__init__()
        self.spac = 640 / (rows * 10)
        self.image = None
        self.mainlayout = QVBoxLayout(self)
        self.paint_area = Maze(self.spac)
        self.mainlayout.addWidget(self.paint_area)
        self.mainlayout.setSpacing(0)
        self.setFixedSize(680, 680)

        self._build_maze(rows, cols)

    def _build_maze(self, num_rows, num_cols):
        M = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)
        image = np.zeros((num_rows * 10, num_cols * 10), dtype=np.uint8)
        r = 0
        c = 0
        history = [(r, c)]
        while history:
            r, c = random.choice(history)
            M[r, c, 4] = 1  # designate this location as visited
            history.remove((r, c))
            check = []
            # If the randomly chosen cell has multiple edges
            # that connect it to the existing maze,
            if c > 0:
                if M[r, c - 1, 4] == 1:
                    check.append('L')
                elif M[r, c - 1, 4] == 0:
                    history.append((r, c - 1))
                    M[r, c - 1, 4] = 2
            if r > 0:
                if M[r - 1, c, 4] == 1:
                    check.append('U')
                elif M[r - 1, c, 4] == 0:
                    history.append((r - 1, c))
                    M[r - 1, c, 4] = 2
            if c < num_cols - 1:
                if M[r, c + 1, 4] == 1:
                    check.append('R')
                elif M[r, c + 1, 4] == 0:
                    history.append((r, c + 1))
                    M[r, c + 1, 4] = 2
            if r < num_rows - 1:
                if M[r + 1, c, 4] == 1:
                    check.append('D')
                elif M[r + 1, c, 4] == 0:
                    history.append((r + 1, c))
                    M[r + 1, c, 4] = 2

            # select one of these edges at random.
            if len(check):
                move_direction = random.choice(check)
                if move_direction == 'L':
                    M[r, c, 0] = 1
                    c = c - 1
                    M[r, c, 2] = 1
                if move_direction == 'U':
                    M[r, c, 1] = 1
                    r = r - 1
                    M[r, c, 3] = 1
                if move_direction == 'R':
                    M[r, c, 2] = 1
                    c = c + 1
                    M[r, c, 0] = 1
                if move_direction == 'D':
                    M[r, c, 3] = 1
                    r = r + 1
                    M[r, c, 1] = 1
        M[0, 0, 0] = 1
        M[num_rows - 1, num_cols - 1, 2] = 1
        # Generate the image for display
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                cell_data = M[row, col]
                for i in range(10 * row + 2, 10 * row + 8):
                    image[i, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[0] == 1:
                    image[range(10 * row + 2, 10 * row + 8), 10 * col] = 255
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 255
                if cell_data[1] == 1:
                    image[10 * row, range(10 * col + 2, 10 * col + 8)] = 255
                    image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[2] == 1:
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 255
                    image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 255
                if cell_data[3] == 1:
                    image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 255
                    image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 255
        self.image = image
        self.paint_area.repaint(self.image, self.spac, self.spac * 2)

    def reset(self):
        pass

    def step(self, action):
        begin = self.paint_area.begin_loc
        begin = [begin[0]+self.spac * 5, begin[1], begin[2], begin[3]]
        self.paint_area.begin_loc = begin
        self.paint_area.repaint(self.image, self.spac, self.spac * 2)

    def render(self):
        pass

    def mousePressEvent(self, QMouseEvent):
        self.step(None)


class Maze(QtWidgets.QWidget):

    def __init__(self, spac):
        super(Maze, self).__init__()
        self.pen = QPen()
        self.painter = QPainter()
        self.painter.setPen(self.pen)
        self.image = None
        self.begin_loc = [0, 0, 0, 0]
        self.spac = spac
        self.begin_loc = [self.spac, self.spac * 4, self.spac * 5, self.spac * 5]
        self.row_len = self.col_len = 0

    def repaint(self, image, row_len, col_len):
        self.image = image
        self.row_len = row_len
        self.col_len = col_len
        self.update()

    def paintEvent(self, e):
        self.painter.begin(self)
        row_len = self.row_len
        col_len = self.col_len
        for _ in self.image:
            for x in _:
                if x == 0:
                    self.painter.setBrush(QColor(0, 0, 0))
                    self.painter.drawRect(row_len, col_len, self.spac, self.spac)
                row_len += self.spac
            row_len = self.spac
            col_len += self.spac
        self.painter.setBrush(QColor(255, 0, 0))
        self.painter.drawEllipse(*self.begin_loc)
        self.painter.end()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MazeEnv()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
