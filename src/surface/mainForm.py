# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created: Sat Aug 12 10:33:23 2017
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainForm(QtGui.QDialog):

    def __init__(self):
        super(Ui_MainForm, self).__init__()
        self.setupUi(self)
        shadow = QtGui.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10);
        shadow.setColor(QtCore.Qt.black);
        shadow.setOffset(2);
        self.setGraphicsEffect(shadow);
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(770, 500)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 768, 482))
        self.widget.setStyleSheet(_fromUtf8("background-image: url(:/img/timg.jpg);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget_2 = QtGui.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 771, 71))
        self.widget_2.setStyleSheet(_fromUtf8("background-image: url(:/img/banner.jpg);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.logo = QtGui.QLabel(self.widget_2)
        self.logo.setGeometry(QtCore.QRect(20, 0, 111, 71))
        self.logo.setAutoFillBackground(False)
        self.logo.setStyleSheet(_fromUtf8("background-image: url(:/img/logo.png);"))
        self.logo.setText(_fromUtf8(""))
        self.logo.setObjectName(_fromUtf8("logo"))
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(630, 10, 71, 51))
        self.label_5.setStyleSheet(_fromUtf8("background-image: url(:/img/head.png);"))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(140, 0, 121, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(_fromUtf8("color: rgb(211, 211, 211);"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 0, 121, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(_fromUtf8("color: rgb(211, 211, 211);"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(380, 0, 121, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(_fromUtf8("color: rgb(211, 211, 211);"))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.widget_2)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 0, 121, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(_fromUtf8("color: rgb(211, 211, 211);"))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.widget_2)
        self.pushButton_5.setGeometry(QtCore.QRect(700, 20, 51, 31))
        self.pushButton_5.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);\n"
"font: 75 14pt \"Agency FB\";\n"
"text-decoration: underline;"))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.widget_3 = QtGui.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(0, 459, 771, 21))
        self.widget_3.setStyleSheet(_fromUtf8("background-image: url(:/img/font.jpg);"))
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.label_7 = QtGui.QLabel(self.widget_3)
        self.label_7.setGeometry(QtCore.QRect(520, 0, 51, 21))
        self.label_7.setStyleSheet(_fromUtf8("color: rgb(255, 255, 0);\n"
"font: 75 10pt \"Agency FB\";"))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.progressBar = QtGui.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(570, 0, 181, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_8 = QtGui.QLabel(self.widget_3)
        self.label_8.setGeometry(QtCore.QRect(50, 0, 54, 21))
        self.label_8.setStyleSheet(_fromUtf8("font: 75 10pt \"Agency FB\";\n"
"color: rgb(255, 170, 0);"))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.tip = QtGui.QLabel(self.widget_3)
        self.tip.setGeometry(QtCore.QRect(110, 1, 401, 20))
        self.tip.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.tip.setObjectName(_fromUtf8("tip"))
        self.file_widget = QtGui.QWidget(self.widget)
        self.file_widget.setGeometry(QtCore.QRect(0, 70, 771, 391))
        self.file_widget.setObjectName(_fromUtf8("file_widget"))

        self.pushButton_5.clicked.connect(self.exit_clicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "文件操作", None))
        self.pushButton_2.setText(_translate("Form", " 聊天室", None))
        self.pushButton_3.setText(_translate("Form", "爬虫", None))
        self.pushButton_4.setText(_translate("Form", "小工具", None))
        self.pushButton_5.setText(_translate("Form", "[退出]", None))
        self.label_7.setText(_translate("Form", "进度条:", None))
        self.label_8.setText(_translate("Form", "信息提示:", None))
        self.tip.setText(_translate("Form", "系统维护中...", None))

    def mouseMoveEvent(self, QMouseEvent):
        if self.z == QtCore.QPoint(): return
        y = QMouseEvent.globalPos()
        x = y - self.z
        self.move(x)

    def mousePressEvent(self, QMouseEvent):
        #鼠标相对于桌面左上角的位置
        y = QMouseEvent.globalPos()
        #窗口左上角相对于桌面左上角的位置
        x = self.geometry().topLeft()
        #z为定值
        self.z = y - x

    def mouseReleaseEvent(self, QMouseEvent):
        self.z = QtCore.QPoint()

    def exit_clicked(self):
        self.close()

import res
