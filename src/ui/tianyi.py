# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tianyi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import random

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class TianYi(QtWidgets.QWidget):

    def __init__(self):
        super(TianYi, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMinimumSize(QtCore.QSize(300, 460))
        self.setMaximumSize(QtCore.QSize(300, 460))
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.label = QtWidgets.QLabel()
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)
        self.move_timer = QtCore.QTimer(self)
        self.flash_timer = QtCore.QTimer(self)
        desk = QtWidgets.QApplication.desktop()
        self.W = desk.width()
        self.H = desk.height()
        self.k = 0
        self.setupUi()

    def setupUi(self):
        self.flash_timer.timeout.connect(self.flash)
        self.flash_timer.start(500)
        self.move_timer.timeout.connect(self.random_move)
        self.move_timer.start(1000)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(_translate("TianYi", "Luo TianYi", None))

    def flash(self):
        if self.k == 0:
            self.label.setStyleSheet(_fromUtf8("background-position:center;\n"
                                                "background-image: url(:/images/tianyi-1.png);\n"
                                                "background-repeat: no-repeat;"))
            self.k += 1
        elif self.k == 1:
            self.label.setStyleSheet(_fromUtf8("background-position:center;\n"
                                               "background-image: url(:/images/tianyi-2.png);\n"
                                               "background-repeat: no-repeat;"))
            self.k += 1
        elif self.k == 2:
            self.label.setStyleSheet(_fromUtf8("background-position:center;\n"
                                               "background-image: url(:/images/tianyi-3.png);\n"
                                               "background-repeat: no-repeat;"))
            self.k += 1
        elif self.k == 3:
            self.label.setStyleSheet(_fromUtf8("background-position:center;\n"
                                               "background-image: url(:/images/tianyi-4.png);\n"
                                               "background-repeat: no-repeat;"))
            self.k = 0

    def random_move(self):
        # 窗口左上角相对于桌面左上角的位置
        x = self.geometry().left()
        y = self.geometry().top()
        self.move(x+random.randrange(-5, 5), y+random.randrange(-5, 5))

    def mouseMoveEvent(self, QMouseEvent):
        if self.z == QtCore.QPoint():
            return
        y = QMouseEvent.globalPos()
        x = y - self.z
        self.move(x)

    def mousePressEvent(self, QMouseEvent):
        #speech.say(u'需要帮助吗,主人')
        # 鼠标相对于桌面左上角的位置
        y = QMouseEvent.globalPos()
        # 窗口左上角相对于桌面左上角的位置
        x = self.geometry().topLeft()
        # z为定值
        self.z = y - x

    def mouseReleaseEvent(self, QMouseEvent):
        self.z = QtCore.QPoint()


import ui.res_rc
