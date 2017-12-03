# -*-coding:utf-8-*-
import sys
from PyQt5 import QtWidgets
from ui.tianyi import TianYi


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = TianYi()
    window.show()
    sys.exit(app.exec_())

##
if __name__ == '__main__':
    main()


