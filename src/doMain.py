import src.ui.loginForm
import sys

from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = src.ui.loginForm.Ui_Form()
    window.show()
    sys.exit(app.exec_())


